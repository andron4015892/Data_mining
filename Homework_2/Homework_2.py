import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://hh.ru'

params = {'area': 1,
          'text': 'Data science',
          'page': 0}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})

print(len(vacancies))
# pprint(dom)
pprint(vacancies)
# <div class="vacancy-serp-item vacancy-serp-item_premium" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_premium"><div class="vacancy-serp-item__row vacancy-serp-item__row_labels"></div><div class=""><div class=""><div class="vacancy-serp-item__row vacancy-serp-item__row_header"><div class="vacancy-serp-item__info"><span data-qa="bloko-header-3" class="bloko-header-section-3 bloko-header-section-3_lite"><span class="resume-search-item__name"><span class="g-user-content"><a class="bloko-link" data-qa="vacancy-serp__vacancy-title" target="_blank" href="https://hh.ru/vacancy/49744980?from=vacancy_search_list&amp;query=data%20scientist" mb-checked="1" data-tip="">Senior data scientist</a></span></span></span></div><div class="vacancy-serp-item__sidebar"><span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-3 bloko-header-section-3_lite">от <!-- -->150 000<!-- --> <!-- -->руб.</span></div></div><div class="vacancy-serp-item__row"><div class="vacancy-serp-item__info"><div class="bloko-text bloko-text_small bloko-text_tertiary"><div class="vacancy-serp-item__meta-info-company"><a class="bloko-link bloko-link_secondary" data-qa="vacancy-serp__vacancy-employer" href="/employer/3151065" mb-checked="1" data-tip="">First data</a></div><div class="vacancy-serp-item__meta-info-badges"><div class="vacancy-serp-item__meta-info-link"><a class="bloko-link" target="_blank" href="https://feedback.hh.ru/article/details/id/5951" mb-checked="1" data-tip=""><span class="bloko-icon bloko-icon_done bloko-icon_initial-action"></span></a></div></div></div><div data-qa="vacancy-serp__vacancy-address" class="bloko-text bloko-text_small bloko-text_tertiary">Москва<!-- -->, <span class="metro-station"><span class="metro-point" style="color:#0072BA"></span>Курская</span> <!-- -->и еще<!-- -->&nbsp;<!-- -->2<!-- -->&nbsp;<span class="metro-station"><span class="metro-point" style="color:#915133"></span></span><span class="metro-station"><span class="metro-point" style="color:#E42313"></span></span></div></div></div></div></div><div class="vacancy-serp-item__row"><div class="vacancy-serp-item__info"><div class="g-user-content"><div data-qa="vacancy-serp__vacancy_snippet_responsibility" class="bloko-text"><span>Проводить A/B-тесты. Участвовать в продуктовом развитии сервиса предиктивной аналитики.</span></div><div data-qa="vacancy-serp__vacancy_snippet_requirement" class="bloko-text bloko-text_no-top-indent"><span>Строить и анализировать customer journey map. Формулировать и проверять гипотезы на основе предыдущих покупок пользователя, пола, возраста и других данных. - </span></div></div></div><div class="vacancy-serp-item__sidebar"><a data-qa="vacancy-serp__vacancy-employer-logo" href="/employer/3151065" mb-checked="1" data-tip=""><img src="https://hhcdn.ru/employer-logo/4088279.jpeg" loading="lazy" alt="First data" class="vacancy-serp-item-logo"></a></div></div><div class="vacancy-serp-item__row vacancy-serp-item__row_controls"><div class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_response"><a class="bloko-button bloko-button_kind-primary bloko-button_scale-small" data-qa="vacancy-serp__vacancy_response" href="/applicant/vacancy_response?vacancyId=49744980&amp;hhtmFrom=vacancy_search_list" mb-checked="1" data-tip=""><span>Откликнуться</span></a></div><span class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_pubdate" data-qa="vacancy-serp__vacancy-date"><span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_long">24&nbsp;ноября</span><span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short">24.11</span></span></div></div>