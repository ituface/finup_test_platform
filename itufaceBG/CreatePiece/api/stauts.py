def status(position):
    '''
    :param position:  lend 推到个贷后状态 oto 状态  PhotoData 拍照项 GraspData 魔蝎抓取项 lend_app 可直接跑的状态
    :return:
    '''
    if position == 'lend':
        return ('APPROVED', 'WAIT_CONTRACT', 'CALM_PERIOD', 'PROCESSING')
    if position == 'oto':
        return ('AUDIT_VIDEO', 'AUDIT_VIDEO_INTERRUPT', 'AUDIT_VIDEO_CONFIRM')
    if position == 'PhotoData':
        return ('ID_PHOTO', 'CAR_DRIVE', 'BUSINESS_SITUATION_CERTIFICATE', 'SOCIAL_SECURITY_FUND', 'CAR_REGISTER',
                'INCOME_PROVE', 'CAR_TRAVEL','OTHER_PROVE','WORK_PROVE','ESTATE_CERTIFICATE','CAR_ANGLE','POLICY_PROVE'
                ,'AMOUNT_CERTIFICATE','MANAGEMENT_PROVE','HOUSEHOLD_REGISTER','AUTOMOBILE_INSURANCE','PROOF_OF_RESIDENCE',
                'BUSINESS_ADDRESS','MARRIAGE_CERTIFICATE','SETTLE_PROVE')
    if position=='GraspData':
        return ('CREDIT_REPORT','OPERATOR_IDENTITY','MAGIC_POLICY','MOXIE_FUND','TAOBAO_IDENTITY','MOXIE_SOCIAL','JD'
                ,'DEGREE_PROVE_MX','PAY_FLOW','ALIPAY')
    if position=='lend_app':
        return ('FAST_LOGIN', 'REGISTER_SUCCESS', 'ANSWER_PRODUCT', 'BASE_INFO', 'SubmitPicture', 'MX_GRAB', 'PUSH_TO_IRON',
         'PUSH_TO_LEND')
    if position=='old_friend_plan':
        return ('FAST_LOGIN', 'REGISTER_SUCCESS', 'ANSWER_PRODUCT')
    if position=='Optimal_plan':
        return ('FAST_LOGIN', 'REGISTER_SUCCESS', 'ANSWER_PRODUCT','BASE_INFO','SubmitPicture','MX_GRAB','PUSH_TO_IRON')
    else:
        return None



print(len(status('PhotoData')))

print(len(status('GraspData')))
