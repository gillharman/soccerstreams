def isMobile(request):
    return request.user_agent.is_mobile or request.user_agent.is_tablet