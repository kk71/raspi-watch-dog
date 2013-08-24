#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
dnspod ddns interface for py3k


original author:im@chuangbo.li
to py3k:kK(fkfkbill@gmail.com)
'''

try:
	import json
except:
	import simplejson as json
from urllib import request
from urllib.parse import urlencode
import re




class ApiCn:
    def __init__(self, email, password, **kw):
        self.base_url = "https://dnsapi.cn"
        self.params = dict(
            login_email=email,
            login_password=password,
            format="json",
        )
        self.params.update(kw)
        self.path = None
    
    def request(self, **kw):
        self.params.update(kw)
        if not self.path:
            #Class UserInfo will auto request path /User.Info.
            name = re.sub(r'([A-Z])', r'.\1', self.__class__.__name__)
            self.path = "/" + name[1:]
        headers={
			"Content-type":"application/x-www-form-urlencoded",
			"Accept":"text/json",
			"User-Agent":"dnspod-python/0.01 (im@chuangbo.li; DNSPod.CN API v2.8)",
        }
        conn=request.Request(url=self.base_url+self.path,
                            data=urlencode(self.params).encode("utf-8"),
                            headers=headers)
        data= request.urlopen(conn,timeout=9).read().decode("utf-8")
        ret = json.loads(data)
        if ret.get("status", {}).get("code") == "1":
            return ret
        else:
            raise Exception(ret)

    __call__ = request
    
class InfoVersion(ApiCn):
    pass

class UserDetail(ApiCn):
    pass

class UserInfo(ApiCn):
    pass

class UserLog(ApiCn):
    pass

class DomainCreate(ApiCn):
    def __init__(self, domain, **kw):
        kw.update(dict(domain=domain))
        ApiCn.__init__(self, **kw)

class DomainId(ApiCn):
    def __init__(self, domain, **kw):
        kw.update(dict(domain=domain))
        ApiCn.__init__(self, **kw)

class DomainList(ApiCn):
    pass

class _DomainApiBase(ApiCn):
    def __init__(self, domain_id, **kw):
        kw.update(dict(domain_id=domain_id))
        ApiCn.__init__(self, **kw)

class DomainRemove(_DomainApiBase):
    pass
        
class DomainStatus(_DomainApiBase):
    def __init__(self, status, **kw):
        kw.update(dict(status=status))
        _DomainApiBase.__init__(self, **kw)
        
class DomainInfo(_DomainApiBase):
    pass
        
class DomainLog(_DomainApiBase):
    pass

class RecordType(ApiCn):
    def __init__(self, domain_grade, **kw):
        kw.update(dict(domain_grade=domain_grade))
        ApiCn.__init__(self, **kw)
        
class RecordLine(ApiCn):
    def __init__(self, domain_grade, **kw):
        kw.update(dict(domain_grade=domain_grade))
        ApiCn.__init__(self, **kw)

class RecordCreate(_DomainApiBase):
    def __init__(self, sub_domain, record_type, record_line, value, ttl, mx=None, **kw):
        kw.update(dict(
            sub_domain=sub_domain,
            record_type=record_type,
            record_line=record_line,
            value=value,
            ttl=ttl,
        ))
        if mx:
            kw.update(dict(mx=mx))
        _DomainApiBase.__init__(self, **kw)

class RecordModify(RecordCreate):
    def __init__(self, record_id, **kw):
        kw.update(dict(record_id=record_id))
        RecordCreate.__init__(self, **kw)
 
class RecordList(_DomainApiBase):
    pass

class _RecordBase(_DomainApiBase):
    def __init__(self, record_id, **kw):
        kw.update(dict(record_id=record_id))
        _DomainApiBase.__init__(self, **kw)

class RecordRemove(_RecordBase):
    pass

class RecordDdns(_DomainApiBase):
    def __init__(self, record_id, sub_domain, record_type, record_line, domain_id, **kw):
        kw.update(dict(
            record_id=record_id,
            sub_domain=sub_domain,
            record_type=record_type,
            record_line=record_line,
			domain_id=domain_id
        ))
        _DomainApiBase.__init__(self, **kw)

class RecordStatus(_RecordBase):
    def __init__(self, status, **kw):
        kw.update(dict(status=status))
        _RecordBase.__init__(self, **kw)

class RecordInfo(_RecordBase):
    pass
