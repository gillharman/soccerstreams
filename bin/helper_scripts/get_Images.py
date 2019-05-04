import requests
from bs4 import BeautifulSoup
import os
import difflib

from teams.models import Team, Team_Logo, Teams_in_League

def go():
    # url = "https://ssl.gstatic.com/onebox/media/sports/logos/z44l-a0W1v5FmgPnemV6Xw_48x48.png"
    matches_html = """
    <div><div jsl="$t t-ppCeFtlodHk;$x 0;" class="r-imgtu6_jn2ms"><table class="ml-bs-u liveresults-sports-immersive__match-grid"><tbody><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81MzI" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQDA" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soAHoECAEQDA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11g0msmf7d" data-mid="/g/11g0msmf7d" data-start-time="2018-12-07T17:30:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 7">12/7</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/04tqw3" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/yggtmgEdp8JilDkQFFfqkA_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/04tqw3" data-dtype="d3sen"><span>Fortuna Sittard</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/0y9j" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/Lhhh1mbsrqH2K1AfXFazrQ_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">3</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/0y9j" data-dtype="d3sen"><span>AZ Alkmaar</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81MzM" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQDQ" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soAXoECAEQDQ"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11g0msmd2n" data-mid="/g/11g0msmd2n" data-start-time="2018-12-07T19:45:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 7">12/7</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/0kqbh" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/kEnNWFGVfOopd7rjZ97-IQ_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">6</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/0kqbh" data-dtype="d3sen"><span>PSV Eindhoven</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/0kq95" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/BV2UdzceQmQPypXQ2Ei_Cg_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/0kq95" data-dtype="d3sen"><span>Excelsior</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81MzQ" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQDg" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soAnoECAEQDg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11f66rl3pb" data-mid="/g/11f66rl3pb" data-start-time="2018-12-08T17:30:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 8">12/8</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/03fnnn" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/RBPXWlwlNXWB0LFJZe0duQ_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/03fnnn" data-dtype="d3sen"><span>Willem II</span><span><img class="imspo_mt__tri" src="//ssl.gstatic.com/onebox/sports/soccer_timeline/red-card-right.svg" align="top" alt="Red Card Icon"></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/037ts6" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/gpKbbIQDYVsiEryIfSWiWQ_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">5</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/037ts6" data-dtype="d3sen"><span>Heerenveen</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81MzU" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQDw" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soA3oECAEQDw"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11ghtnn799" data-mid="/g/11ghtnn799" data-start-time="2018-12-08T18:45:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 8">12/8</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/03kvkj" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/wG9B0Qx4RzFdcpLmKnjHLQ_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/03kvkj" data-dtype="d3sen"><span>Zwolle</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/0y54" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/4b9b9O2fDwJepsLnYEoZng_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">4</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/0y54" data-dtype="d3sen"><span>Ajax</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81MzY" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQEA" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soBHoECAEQEA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11f66rm3m6" data-mid="/g/11f66rm3m6" data-start-time="2018-12-08T19:45:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 8">12/8</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/015f47" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/DNIfTEANNhUd5m6iHupoKw_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/015f47" data-dtype="d3sen"><span>Den Haag</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/04jbyg" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/Q4Y5fb7Oh8fyAedgd4aRGA_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/04jbyg" data-dtype="d3sen"><span>De Graafschap</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81Mzc" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQEQ" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soBXoECAEQEQ"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11g0msnj3b" data-mid="/g/11g0msnj3b" data-start-time="2018-12-09T11:15:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 9">12/9</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/03fnmd" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/IhISAI5vMGlCbfHdiv9_Rg_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">3</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/03fnmd" data-dtype="d3sen"><span>Utrecht</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/06q02g" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/EDWW-98PyPcSLD3Qm2oZZg_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/06q02g" data-dtype="d3sen"><span>Heracles</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81Mzg" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQEg" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soBnoECAEQEg"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11g0msm_wm" data-mid="/g/11g0msm_wm" data-start-time="2018-12-09T13:30:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 9">12/9</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/06qm95" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/VIjbNerVnpHgQ4wWWmVBnA_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/06qm95" data-dtype="d3sen"><span>FC Emmen</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/0cttx" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/36g41WN3WdjCRsSFiurazw_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">4</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/0cttx" data-dtype="d3sen"><span>Feyenoord</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81Mzk" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQEw" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soB3oECAEQEw"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11ghtnmykh" data-mid="/g/11ghtnmykh" data-start-time="2018-12-09T13:30:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 9">12/9</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/06vlk0" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/HAmlPNNf_0Zc8hGN6UBKhA_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/06vlk0" data-dtype="d3sen"><span>VVV</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/0466hh" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/jxhOCPcsmcO7tRwVf12mcg_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">0</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/0466hh" data-dtype="d3sen"><span>Groningen</span><span></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td></tr><tr><td class="liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-right-border"><div jscontroller="Fcsp7c" class="imso-hov" style="outline:none" jsdata="kGLyrd;;B81Mzo" role="link" tabindex="0" jsaction="rcuQ6b:npT2md;JqlOve" data-hveid="CAEQFA" data-ved="2ahUKEwj33f2k0ObgAhXC8YMKHei7BKgQt0soCHoECAEQFA"><div class="imso-loa DbuNre imso-ani" data-df-match-mid="/g/11f66rl8vz" data-mid="/g/11f66rl8vz" data-start-time="2018-12-09T15:45:00Z"><div class="imspo_mt__mtc-no"><table class="imspo_mt__mit"><tbody><tr class="imspo_mt__tr-s"><td class="lc"></td><td></td><td class="imspo_mt__rg"></td><td class="imspo_mt__sc-sp"></td><td class="imspo_mt__sc"></td><td class="imspo_mt__rpo-c" style="width:0px"></td></tr><tr><td class="imspo_mt__lg-st-c" colspan="6"></td></tr><tr><td colspan="3"></td><td class="imspo_mt__sc-spc" rowspan="5"></td><td rowspan="5" class="imspo_mt__match-sc imspo_mt__wt"><div class="imspo_mt__ms-w"><div class="imso-medium-font"><div class="imspo_mt__cm-s imspo_mt__ndl-p imso-medium-font imspo_mt__match-status" aria-label="Full-time score">FT</div><div class="imspo_mt__cmd"><span aria-label="December 9">12/9</span></div></div></div></td><td></td></tr><tr><td></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/02jgm0" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/5QzjC5uajTeyHE_fjTlWSQ_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__dt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">2</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/02jgm0" data-dtype="d3sen"><span>NAC</span><span></span></div></td><td class="imspo_mt__rg"><svg class="imspo_mt__triangle" aria-label="Winner" height="8" role="img" width="6"><polygon points="6,0 6,8 0,4" style="fill:black"></polygon></svg></td></tr><tr class="imspo_mt__tr"><td class="kno-fb-ctx imspo_mt__lgc lc" data-df-team-mid="/m/03fnn5" data-dtype="d3sel"><img src="//ssl.gstatic.com/onebox/media/sports/logos/MvgDWCCFiHLV9-uBdw704g_48x48.png" alt="" style="width:24px;height:24px"></td><td class="tns-c imspo_mt__tt-w imspo_mt__lt-t"><div class="imspo_mt__t-sc"><div class="imspo_mt__tt-w">1</div></div><div class="ellipsisize kno-fb-ctx" data-df-team-mid="/m/03fnn5" data-dtype="d3sen"><span>Vitesse</span><span><img class="imspo_mt__tri" src="//ssl.gstatic.com/onebox/sports/soccer_timeline/red-card-right.svg" align="top" alt="Red Card Icon"></span></div></td><td class="imspo_mt__rg"></td></tr><tr><td></td></tr><tr class="imspo_mt__br-s"></tr></tbody></table></div></div></div></td><td class="liveresults-sports-immersive__empty-tile"></td></tr></tbody></table></div></div>
    """
    html = BeautifulSoup(matches_html, features="html.parser")

    r = html.find_all('img',attrs={"style":"width:24px;height:24px"})

    teams = []
    for i in r:
        parent = i.parent.parent
        team = parent.find_all('span')[0].string
        team_name = team.lower().replace(' ','_')
        xname = team_name + '_48x48.png'
        url = "https:" + i['src']
        pic = requests.get(url).content
        f = open('logos/' + xname, 'wb')
        f.write(pic)
        f.close()

        yname = team_name + '_96x96.png'
        url = url.replace('48x48', '96x96')
        pic = requests.get(url).content
        f = open('logos/' + yname, 'wb')
        f.write(pic)
        f.close()

        team_info = {}
        team_info["team"] = team
        team_info["48x48"] = xname
        team_info["96x96"] = yname
        teams.append(team_info)

    print('Total Images: ' + str(len(r)))
    return teams

def a(g_teams, league_code):
    os.chdir("logos")
    teams = Teams_in_League.objects.filter(league__code=league_code).values_list('team__short_name', flat=True)
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