from rest_framework.response import Response
from rest_framework.views import APIView


class TodoView(APIView):
    user_id=''
    version=''

    def dispatch(self, request, *args, **kwargs):
        self.user_id=request.headers.get('user_id',False)
        self.version=request.headers.get('version',False)
        return super(TodoView,self).dispatch(request, *args, **kwargs)

    
def SuccessResponse():
    return Response(status=200,
                    data=dict(
                        result_code=0,
                        result_msg="success"
                    ))


def SuccessResponseWithData(data):
    return Response(status=200,
                    data=dict(
                        result_code=0,
                        result_msg="success",
                        data=data
                    ))


def ErrorResponse():
    return Response(status=200,
                    data=dict(
                        result_code=999,
                        result_msg="error!!!"
                    ))
def CommonResponse(result_code, result_msg, data):
    return Response(status=200,
                    data=dict(
                        result_code=result_code,
                        result_msg=result_msg,
                        data=data
                        )
                    )