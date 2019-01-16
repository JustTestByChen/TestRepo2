#!/usr/bin/env python
#-*- coding:utf-8 -*-
###############################################################################
#Copyright(C),2012,BEST LOGISTICS TECHNOLOGY(CHINA) Co., LTD.
#
# Filename: P0096_payment_query.py
# Version:     1.0.0
# Description: 验证待对账采购订单经销对账单，采退订单经销对账单查询结果
# Author:      Xu Qin
###############################################################################
import logging,ophttpctrl,datetime,time
from ediclient import builder
from dianjia_bvt_case.common import base_page
from dianjia_bvt_case.util.purchase.distribute_finish_const import FinishCoust
from autobench_init.dianjia_autobench import autobench
from bsatf.bat_test import TestCase,CaseInfo
from bsatf.bat_result import ResultNote
from dianjia_bvt_case.util.app_flow_const import AppFlowConst as account

class PaymentQuery(TestCase):
    def __init__(self):
        TestCase.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        #定义基本信息
        self.case_info = CaseInfo()
        self.case_info.name="payment_query"
        self.case_info.id="P0096"
        self.case_info.author = "Xu Qin"
        self.case_info.version='1.0.0'
        self.case_info.description= u'''
        step1:根据区域查询
        step2:根据供应商查询
        step3:根据合同类型查询
        step4:根据区域、供应商、合同类型查询
        step5:根据区域查询未对账采退单
        step6:根据供应商查询未对账采退单
        step7:根据合同类型查询未对账采退单
        step8:根据区域、供应商、合同类型查询未对账采退单
        '''
    def add_task(self):
        self.register_case(self.payment_query,self.case_info)
    def payment_query(self):
        test_result = ResultNote()
        #定义OPCtrl
        self.opbvt = ophttpctrl.Builder()
        self.edi = builder()

        user_admin=account.admin_user
        psw_admin=account.admin_psw
        createdBeginDate=str(datetime.date.today())+' 00:00'
        createdEndDate=str(datetime.date.today() + datetime.timedelta(days=1))+' 00:00'

        try:
            self.djop.auth.login(username=user_admin, password=psw_admin)
            districtId=600643
            supplierCode=00210
            contractCode='HT1700169'
            self.logger.step(u'step1:根据区域查询')
            response=self.opbvt.pay_request.pending_payment_query(districtId=districtId,supplierCode=supplierCode,contractCode=contractCode,inboundBeginDate=createdBeginDate,inboundEndDate=createdEndDate)
            payment_info=base_page.db_sql_query('select * from djo_purchase_order where district_id=\'{0}\' and supplier_code=\'{1}\' and contract_code=\'{2}\' and created_time between \'{3}\' and \'{4}\' and (INBOUND_STATUS=\'INBOUNDED\' or INBOUND_STATUS=\'INBOUNDING\') and verify_status=\'NOT_VERIFY\''.format(districtId,supplierCode,contractCode,createdBeginDate,createdEndDate))
            if len(response)!=len(payment_info):
                self.break_test(u'根据区域接口和数据库查询个数不一致!') 
            for i in xrange(len(payment_info)):
                for j in xrange(len(response)):
                    if payment_info[i]['code'] in response[j]['code']:
                        break
                else:
                    self.break_test(u'区域查询，接口查询结果的订单号{0}，未在数据库中查到.'.format(payment_info['code']))
            self.logger.step(u'step2:根据区域查询未对账采退单')
            response=self.opbvt.pay_request.pending_return_payment_query(districtId=districtId,supplierCode=supplierCode,contractCode=contractCode,outboundBeginDate=createdBeginDate,outboundEndDate=createdEndDate)
            payment_info=base_page.db_sql_query('select * from djo_purchase_return_order where district_id=\'{0}\' and supplier_code=\'{1}\' and contract_code=\'{2}\' and created_time between \'{3}\' and \'{4}\'  and verify_status=\'NOT_VERIFY\''.format(districtId,supplierCode,contractCode,createdBeginDate,createdEndDate))
            if len(response)!=len(payment_info):
                self.break_test(u'根据区域接口和数据库查询个数不一致!') 
            for i in xrange(len(payment_info)):
                for j in xrange(len(response)):
                    if payment_info[i]['code'] in response[j]['code']:
                        break
                else:
                    self.break_test(u'区域查询，接口查询结果的订单号{0}，未在数据库中查到.'.format(payment_info['code']))
            passfail=ResultNote.PASS
            test_comment=u"{0}经销对账单，经销采退单查询成功.".format(self.case_info.id) 
        except Exception, Err:
            passfail=ResultNote.FAIL
            test_comment = u"{0},{1}.".format(self.case_info.id,Err) 
        finally:
            test_result.record_result(passfail=passfail,test_comment=test_comment)
            return test_result
    def clean_test(self):
        self.logger.debug("clean test...")
        self.logger.debug("clean test over.")

    a = "to be or not to be, it's a problem"
        