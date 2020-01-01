import requests
from bs4 import BeautifulSoup
import os
import difflib

from teams.models import Team, Team_Logo

def go(league_code):
    # url = "https://ssl.gstatic.com/onebox/media/sports/logos/z44l-a0W1v5FmgPnemV6Xw_48x48.png"
    # matches_html = """
    # <table class="ml-bs-u liveresults-sports-immersive__match-grid"><tbody><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KR0" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQOg" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soAHoECAEQOg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11fm6nvvd7" data-mid="/g/11fm6nvvd7" data-start-time="2019-12-20T20:00:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Friday, December 20">Fri, 12/20</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:30" href="https://www.youtube.com/watch?v=TlDPLQahD5M&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DTlDPLQahD5M%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEDs"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/a0Hr4YaLf8gn4Udj_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:30</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/06z9k8"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/sbTFnFgPeUsTa-szphHf8Q_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">3</div></div><div class="ellipsisize" data-df-team-mid="/m/06z9k8"><span>Eibar</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/0f5hyg"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/Fn_X2IO4-1ACuTemcHkDEw_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize" data-df-team-mid="/m/0f5hyg"><span>Granada</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KR4" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQPA" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soAXoECAEQPA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11hz2kf__q" data-mid="/g/11hz2kf__q" data-start-time="2019-12-21T12:00:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Saturday, December 21">Sat, 12/21</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=6c-MPoHMjxM&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3D6c-MPoHMjxM%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBED0"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/CQSDR67d59gCTQFl_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/01vqc7"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/Ss21P4CUmigjrEtcoapjVg_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize" data-df-team-mid="/m/01vqc7"><span>RCD Mallorca</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/01k9cc"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/hCTs5EX3WjCMC5Jl3QE4Rw_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">2</div></div><div class="ellipsisize" data-df-team-mid="/m/01k9cc"><span>Sevilla</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KR8" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQPg" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soAnoECAEQPg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11hz2k9yzs" data-mid="/g/11hz2k9yzs" data-start-time="2019-12-21T15:00:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Saturday, December 21">Sat, 12/21</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=ZJD5lOlLX1M&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DZJD5lOlLX1M%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBED8"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/xduklRWDr69PAP3W_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/0hvgt"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/paYnEE8hcrP96neHRNofhQ_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">4</div></div><div class="ellipsisize" data-df-team-mid="/m/0hvgt"><span>Barcelona</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/03tcwm"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/meAnutdPID67rfUecKaoFg_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize" data-df-team-mid="/m/03tcwm"><span>Alavés</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSA" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQQA" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soA3oECAEQQA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11fm6pln_t" data-mid="/g/11fm6pln_t" data-start-time="2019-12-21T17:30:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Saturday, December 21">Sat, 12/21</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=R00Ci7YxyrQ&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DR00Ci7YxyrQ%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEEE"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/U-aXiJBQDTKNkCOz_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/03tck1"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/WKH7Ak5cYD6Qm1EEqXzmVw_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize" data-df-team-mid="/m/03tck1"><span>Villarreal</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/03tc8d"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/1UDHZMdKZD15W5gus7dJyg_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize" data-df-team-mid="/m/03tc8d"><span>Getafe CF</span><span><img class="imspo_mt__tri" src="//ssl.gstatic.com/onebox/sports/soccer_timeline/red-card-right.svg" alt="Red cards" align="top"></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSE" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQQg" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soBHoECAEQQg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11hz2kf__s" data-mid="/g/11hz2kf__s" data-start-time="2019-12-21T20:00:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Saturday, December 21">Sat, 12/21</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=9CLpIVt8dQc&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3D9CLpIVt8dQc%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEEM"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/P9ZMfHs6xYsNxXUL_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/01r5xw"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/HlIrXZRP96tv0H1uiiN0Jg_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize" data-df-team-mid="/m/01r5xw"><span>Valladolid</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/080_y"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/QPbjvDwI_0Wuu4tCS2O6uw_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize" data-df-team-mid="/m/080_y"><span>Valencia</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSI" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQRA" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soBXoECAEQRA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11h4g7jmkf" data-mid="/g/11h4g7jmkf" data-start-time="2019-12-22T11:00:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Sunday, December 22">Sun, 12/22</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=zIl2Bdk3Nes&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DzIl2Bdk3Nes%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEEU"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/MxfvSk7HK_A3k9n6_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/072xw8"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/Id84F7Ji9rZGVacaazlBYA_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">2</div></div><div class="ellipsisize" data-df-team-mid="/m/072xw8"><span>Leganes</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/025txtg"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/TKitIqelDyN6M-kYt4Uc0g_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize" data-df-team-mid="/m/025txtg"><span>Espanyol</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSM" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQRg" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soBnoECAEQRg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11h4g7kr_p" data-mid="/g/11h4g7kr_p" data-start-time="2019-12-22T13:00:00Z" style=""><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Sunday, December 22">Sun, 12/22</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=QlGOi8WYtZQ&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DQlGOi8WYtZQ%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEEc"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/a3nifXprWFyu4wP2_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/03tc5p"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/pk-hNCNpGM_JDoHHvLVF-Q_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">3</div></div><div class="ellipsisize" data-df-team-mid="/m/03tc5p"><span>Osasuna</span><span><img class="imspo_mt__tri" src="//ssl.gstatic.com/onebox/sports/soccer_timeline/red-card-right.svg" alt="Red cards" align="top"></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/0122wc"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/w8tb1aeBfVZIj9tZXf7eZg_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">4</div></div><div class="ellipsisize" data-df-team-mid="/m/0122wc"><span>Real Sociedad</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSQ" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQSA" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soB3oECAEQSA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11hz2k1yj6" data-mid="/g/11hz2k1yj6" data-start-time="2019-12-22T15:00:00Z" style=""><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Sunday, December 22">Sun, 12/22</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=XmWui3RvHAE&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DXmWui3RvHAE%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEEk"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/b2cyUKGiueMoowPE_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/03fnqj"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/S0fDZjYYytbZaUt0f3cIhg_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize" data-df-team-mid="/m/03fnqj"><span>Real Betis</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/0lg7v"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/srAAE0bOnCppUrlbJpFiHQ_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">2</div></div><div class="ellipsisize" data-df-team-mid="/m/0lg7v"><span>Atlético Madrid</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="lr-imso-scroll liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSU" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQSg" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soCHoECAEQSg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11hz2jss3w" data-mid="/g/11hz2jss3w" data-start-time="2019-12-22T17:30:00Z" style=""><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Sunday, December 22">Sun, 12/22</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=qFSAB46BB3Q&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DqFSAB46BB3Q%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEEs"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/I4ZqVfVgbt6FMDWP_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/01njml"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/SQB-jlVosxVV1Ce79FhbOA_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">3</div></div><div class="ellipsisize" data-df-team-mid="/m/01njml"><span>Levante</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/0266sb_"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/wpdhixHP_sloegfP0UlwAw_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize" data-df-team-mid="/m/0266sb_"><span>Celta Vigo</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;At4KSY" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQTA" data-ved="2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQt0soCXoECAEQTA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11h4g7qby1" data-mid="/g/11h4g7qby1" data-start-time="2019-12-22T20:00:00Z" style=""><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="Sunday, December 22">Sun, 12/22</span></div></div></div><div class="imspo_mt__vr-tc imspo_mt__ndl-p"><div jsaction="jsa.true" style="position:relative"><a aria-label="Match recap · 1:31" href="https://www.youtube.com/watch?v=xPRVDdL3j3A&amp;feature=onebox" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.youtube.com/watch%3Fv%3DxPRVDdL3j3A%26feature%3Donebox&amp;ved=2ahUKEwjarIya4dTmAhWGHc0KHfZYD4gQs056BAgBEE0"><img class="imspo_mt__vti" src="//ssl.gstatic.com/onebox/media/sports/videos/liga/1ECQwb5UNHE7A7iI_192x108.jpg" alt=""><span class="imspo_mt__vol imspo_mt__vtb imspo_mt__vdo" aria-hidden="true">► 1:31</span></a></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/06l22"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/Th4fAVAZeCJWRcKoLW7koA_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize" data-df-team-mid="/m/06l22"><span>Real Madrid</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="imspo_mt__lgc lc" data-df-team-mid="/m/0kwv2"><img class="imso_btl__mh-logo" alt="" src="//ssl.gstatic.com/onebox/media/sports/logos/OSL_5Zm6kYPP1J17Bo5uDA_48x48.png" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize" data-df-team-mid="/m/0kwv2"><span>Ath. Bilbao</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr></tbody></table>
    # """
    # os.chdir("data/")
    html_file = open("data/logos_html.txt", "r")
    matches_html = str(html_file.read())
    html_file.seek(0)
    html_file.close()
    html = BeautifulSoup(matches_html, features="html.parser")

    r = html.find_all('img',attrs={"style":"width:24px;height:24px"})

    images = 0
    teams = []
    teams_id_in_leagues = set(Team.objects.filter(leagues__code=league_code).values_list('id', flat=True))
    teams_id_with_logos = set(Team_Logo.objects.filter(team__leagues__code=league_code).values_list('team_id', flat=True))
    teams_without_logos = teams_id_in_leagues - teams_id_with_logos
    team_name_without_logos = Team.objects.filter(id__in=teams_without_logos).values_list('short_name', flat=True)
    for i in r:
        parent = i.parent.parent
        try:
            team = parent.find_all('span')[0].string
        except IndexError as e:
            print(e.__str__())
            continue

        m = difflib.get_close_matches(team, team_name_without_logos, n=1)
        if m:
            team_name = team.lower().replace(' ','_')
            xname = team_name + '_48x48.png'
            url = "https:" + i['src']
            pic = requests.get(url).content
            f = open('data/logos/' + xname, 'wb')
            f.write(pic)
            images = images + 1
            f.close()

            yname = team_name + '_96x96.png'
            url = url.replace('48x48', '96x96')
            pic = requests.get(url).content
            f = open('data/logos/' + yname, 'wb')
            f.write(pic)
            images = images + 1
            f.close()

            team_info = {}
            team_info["team"] = team
            team_info["48x48"] = xname
            team_info["96x96"] = yname
            teams.append(team_info)

    print('Total Images: ' + str(images))
    # os.chdir("..")
    return teams

def a(g_teams, league_code):
    os.chdir("data/logos")
    teams = Team.objects.filter(leagues__code=league_code).values_list('short_name', flat=True)
    skipped_teams = []
    for i in g_teams:
        m = difflib.get_close_matches(i["team"], teams, n=1)
        try:
            print('Match Found: ' + i["team"] + ' = ' + m[0])
            team = Team.objects.filter(short_name=m[0]).first()
            name = m[0].lower().replace(' ', '_')
            save_logo(team, name, i)
        except:
            print('No match found for ' + i["team"])
            skipped_teams.append(i)

    if skipped_teams:
        #EXPAND THE SEARCH AND TRY AGAIN
        for skipped_team in skipped_teams:
            try:
                m = difflib.get_close_matches(skipped_team["team"], teams, n=20, cutoff=1)
                print('Expanding Search..')
                print(m)
                index = input('Select: ')
                team = Team.objects.filter(short_name=m[index]).first()
                name = m[index].lower().replace(' ', '_')
                save_logo(team, name, skipped_team)
            except:
                raise
                print('No decent matches found for: ' + skipped_team["team"])

    os.chdir("../..")


def save_logo(team, name, o):
    t = Team_Logo()
    t.team = team
    t.logo_48x48 = name + '_48x48.png'
    t.logo_48x48_url = t.logo_48x48.url
    t.logo_96x96 = name + '_96x96.png'
    t.logo_96x96_url = t.logo_96x96.url
    t.save()

    #RENAME LOGO FILE NAMES
    try:
        os.rename(o["48x48"], t.logo_48x48.name)
        os.rename(o["96x96"], t.logo_96x96.name)
    except:
        print("Files not renamed for " + t.logo_48x48.name + ' and ' + t.logo_96x96.name)


def wd():
    print(os.getcwd())


def updateLogoUrls():
    logos = Team_Logo.objects.all()
    for i in logos:
        team_logo = Team_Logo.objects.get(id=i.id)
        team_logo.logo_48x48_url = "https://storage.googleapis.com/team_logos/" + team_logo.logo_48x48.name
        team_logo.logo_96x96_url = "https://storage.googleapis.com/team_logos/" + team_logo.logo_96x96.name
        team_logo.save()


def updateLogos(logos):
    for logo in logos:
        name_split = logo["name"].split('-')
        name = name_split[0]
        print('Name: ' + name)
        if '48x48' in name_split:
            team_logo = Team_Logo.objects.filter(logo_48x48__contains=name).first()
            print('Filter results from 48x48: ')
            print(team_logo)
            if team_logo:
                new_logo = logo["name"] + "." + logo["ext"]
                new_logo_url = "https://i.postimg.cc/" + logo["hotlink"] + "/" + new_logo
                print('New logo: ' + new_logo)
                print('New Logo URL: ' + new_logo_url)
                team_logo.logo_48x48 = new_logo
                team_logo.logo_48x48_url = new_logo_url
                team_logo.save()
            else:
                print('Unable to update 48x48 logo using ' + logo["name"])

        else:
            team_logo = Team_Logo.objects.filter(logo_96x96__contains=name).first()
            print('Filter results from 96x96: ')
            print(team_logo)
            if team_logo:
                new_logo = logo["name"] + "." + logo["ext"]
                new_logo_url = "https://i.postimg.cc/" + logo["hotlink"] + "/" +  new_logo
                print('New logo: ' + new_logo)
                print('New Logo URL: ' + new_logo_url)
                team_logo.logo_96x96 = new_logo
                team_logo.logo_96x96_url = new_logo_url
                team_logo.save()
            else:
                print('Unable to update 96x96 logo using ' + logo["name"])

    return True


def extractLogoImagesInfo(html):
    soup = BeautifulSoup(html)
    divs = soup.find_all("div", class_="thumb_container")
    logos_info = []
    for div in divs:
        logo_info = {}
        logo_info["hotlink"] = div["data-hotlink"]
        logo_info["name"] = div["data-name"]
        logo_info["ext"] = div["data-ext"]
        logos_info.append(logo_info)

    return logos_info