# coding=utf-8


class ServerException(Exception):
    """
        服务器异常
    """
    pass


class IgnoreException(Exception):
    """
        忽略异常
    """
    pass


class PhoneSmsLockException(ServerException):
    """
        发送短信验证码busy
    """
    pass


class InvalidInviteCustomer(IgnoreException):
    """
        错误的邀请人
    """
    pass


class ValidationError(ServerException):
    """
        value 异常
    """
    pass


class ClientLoginException(ServerException):
    """ 客户端登录异常  """
    pass


class ReqException(ServerException):
    """请求异常"""
    pass