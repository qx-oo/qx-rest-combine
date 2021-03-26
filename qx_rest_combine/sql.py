from threading import local
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI
from django.core.exceptions import EmptyResultSet


_thread_locals = local()


def execute_sql(self, result_type=MULTI, chunked_fetch=False, **kwargs):
    if hasattr(_thread_locals, 'query_cache'):
        try:
            sql, params = self.as_sql()
            if not sql:
                raise EmptyResultSet
            if params:
                sql = sql % params
        except EmptyResultSet:
            if result_type == MULTI:
                return iter([])
            else:
                return
        if sql[:6].upper() == 'SELECT':
            ret = _thread_locals.query_cache.get(sql)
            if ret:
                return ret
            ret = self._qx_execute_sql(
                result_type=result_type, chunked_fetch=False, **kwargs)
            _thread_locals.query_cache[sql] = ret
            return ret
        else:
            _thread_locals.query_cache = {}
    return self._qx_execute_sql(
        result_type=result_type, chunked_fetch=chunked_fetch, **kwargs)


if not hasattr(SQLCompiler, '_qx_execute_sql'):
    SQLCompiler._qx_execute_sql = SQLCompiler.execute_sql
    SQLCompiler.execute_sql = execute_sql
