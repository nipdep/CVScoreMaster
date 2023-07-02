from heapq import nsmallest
from turtle import width
from h2o_wave import Q, app, ui, data

from .utilities import load_cv_data, load_js_data, load_model, load_short_list, load_llm

config = {
    "app_title": "CV ScoreMaster",
    "sub_title": "Automated CV Shortlisting and Scoring for Job Applications",
    "footer_text": 'Copyright 2023, Made using <a href="https://wave.h2o.ai" target="_blank">H2O Wave</a>',
    'description': "CV ScoreMaster is a cutting-edge web application that revolutionizes the recruitment process by automating the CV shortlisting and scoring process. Our advanced algorithms analyze job descriptions and CVs to provide an efficient and objective evaluation of candidates. Save time and resources by effortlessly identifying the most qualified candidates for your job openings. With CV ScoreMaster, streamline your hiring process and make data-driven decisions to find the perfect fit for your organization."
}


async def initialize_app(q):
    q.user.font_color = '#fec827'
    q.user.primary_color = '#fec827'
    q.page['meta'] = ui.meta_card(box='')
    if q.user.config is None:
        q.user.config = config
        q.user.default_config = config
        q.client.selected_tab = 'home_tab'

    if q.user.logo is None:
        q.user.logo, = await q.site.upload(['static/logo.png'])
        q.user.logo_height = '50'

    if q.app.illustration is None:
        q.app.illustration, = await q.site.upload(['static/ill1.jpg'])

    if q.app.jd_ill is None:
        q.app.jd_ill, = await q.site.upload(['static/tok2.jpg'])

    if q.app.jd_image is None:
        q.app.jd_image, = await q.site.upload(['static/tok3.jpeg'])

    if q.app.jd_icon is None:
        q.app.jd_icon, = await q.site.upload(['static/jd.png'])

    if q.app.user_icon is None:
        q.app.user_icon, = await q.site.upload(['static/cv.png'])

    if q.app.loader is None:
        q.app.loader, = await q.site.upload(['static/PG1.gif'])

    if q.user.emb_model is None:
        q.user.emb_model = load_model()

    if q.user.llm is None:
        q.user.llm = load_llm()

    if q.user.jds is None:
        q.user.jds = load_js_data()

    if q.user.cvs is None:
        q.user.cvs = load_cv_data()

    if q.user.sl_cvs is None:
        q.user.sl_cvs = load_short_list()

    q.user.init = True


def create_layout(q: Q, tag=None):
    config = q.user.config
    q.page.drop()

    q.page['header'] = ui.header_card(
        box='header',
        title=config['app_title'],
        subtitle=config['sub_title'],
        icon='TFVCLogo',
        icon_color='#222',
        items=[
            ui.button(name='home_tab', label=' ', icon='Home',
                      primary=True, width='40px'),
            ui.button(name='about_tab', label=' ',
                      icon='info', primary=True, width='40px'),
            ui.button(name='setting_tab', label=' ',
                      icon='Settings', primary=True, width='40px'),
            ui.text(
                """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
                """
            ),
            ui.text("<img src='"+q.user.logo+"' width='" +
                    str(q.user.logo_height)+"px'>"),
        ],

    )
    # nav_items =
    if q.client.generate_dashboard:
        nav_items += [
            ui.tab(name='#', label='', icon='BulletedListBulletMirrored'),
            ui.tab(name='dashboard_tab', label='Dashboard', icon='Processing'),
        ]

    # navbar_items = [ui.inline(items=[
    #     ui.tabs(name='tabs', value=q.args.tabs, link=True, items=nav_items)
    # ])]

    # q.page['navbar'] = ui.form_card(box=ui.box(
    #     zone='navbar'), title='', items=navbar_items)
    q.page['footer'] = ui.footer_card(
        box='footer', caption=config['footer_text'])

    zones = ui.zone(name='content', zones=[ui.zone(
        name='content_0', size='650px', direction='row')])
    if tag in ['feature']:
        zones = ui.zone(name='content', zones=[
            ui.zone(name='content_0', size='600px', direction='row'),
            ui.zone(name='content_1', size='500px', direction='row'),

        ])
    elif tag == 'setting':
        zones = ui.zone(name='content', zones=[
            ui.zone(name='content_1', size='300px', direction='row'),
            ui.zone(name='content_0', size='80px', direction='row'),

        ])
    elif tag in ['launch', 'jd']:
        zones = ui.zone(name='content', direction='row',  # size='560px',
                        zones=[
                            ui.zone(name='content_0', size='35%',
                                    direction='column'),
                            ui.zone(name='content_1', size='65%', direction='column',
                                    # zones=[
                                    # ui.zone(name='content_1', size='25%', direction='row'),
                                    # ui.zone(name='content_2', size='75%', direction='column')
                                    # ]
                                    )
                        ])
    elif tag in ['cv']:
        zones = ui.zone(name='content', direction='row',  # size='560px',
                        zones=[
                            ui.zone(name='content_0', size='35%',
                                    direction='column'),
                            ui.zone(name='content_01', size='65%', direction='column',
                                    zones=[
                                    ui.zone(name='content_001', size='25%', direction='row', zones=[
                                        ui.zone(name='content_1', size='35%', direction='column'),
                                        ui.zone(name='content_2', size='65%', direction='column')
                                    ]),
                                    ui.zone(name='content_3', size='75%', direction='column')
                                    ]
                                )
                        ])
    elif tag == 'home':
        # zones = ui.zone(name='content_0', size='650px')
        zones = ui.zone(name='content', direction='row',  # size='560px',
                        zones=[
                            ui.zone(name='content_0'),
                        ])

    else:
        print(tag)
        pass

    q.page['meta'] = ui.meta_card(box='',
                                  themes=[
                                      ui.theme(
                                          name='cdark',
                                          primary=q.user.primary_color,
                                          text=q.user.font_color,
                                          card='#000',
                                          page='#1b1d1f',
                                      ),
                                      ui.theme(
                                            name='ixdlabs_twitter',
                                            primary='#330952',
                                            text='#000000',
                                            card='#ffffff',
                                            page='#e4d0f2',
                                      )
                                  ],
                                  theme='ixdlabs_twitter',
                                  title=config['app_title'],
                                  # stylesheet=ui.inline_stylesheet(style),
                                  layouts=[
                                      ui.layout(
                                          breakpoint='xl',
                                          width='100%',
                                          zones=[
                                              ui.zone(
                                                  name='header', size='75px', direction='row'),
                                              #   ui.zone(
                                                #   name='navbar', size='90px', direction='row'),
                                              zones,
                                              ui.zone('footer'),
                                          ])
                                  ])


async def render_template(q: Q, page_cfg):
    create_layout(q, tag=page_cfg['tag'])

    if page_cfg['tag'] == 'home':
        caption = """<div style='width:70%;margin-left:15%'>"""
        caption += """CV ScoreMaster is a cutting-edge web application that revolutionizes the recruitment process by automating the CV shortlisting and scoring process. Our advanced algorithms analyze job descriptions and CVs to provide an efficient and objective evaluation of candidates. Save time and resources by effortlessly identifying the most qualified candidates for your job openings. With CV ScoreMaster, streamline your hiring process and make data-driven decisions to find the perfect fit for your organization.
		"""
        # caption += f"<br><br><img src='{q.app.caption}' width='80%' height='200px'>"
        caption += "<br><hr></div>"
        q.page['content_left'] = ui.tall_info_card(
            box=ui.box(zone='content_0', height='700px'),
            name='launch_app',
            title=config["app_title"],
            caption=caption,
            category=config["sub_title"],
            label='Launch',
            image=q.app.illustration,
            image_height='180px'
        )
    elif page_cfg['tag'] == 'about':
        q.page['content_00'] = ui.form_card(box=ui.box(
            zone='content_0', width='100%', order=1), title='', items=[])

    elif page_cfg['tag'] == 'dashboard':
        q.page['content_00'] = ui.form_card(box=ui.box(
            zone='content_0', width='100%', order=1), title='', items=[])

    elif page_cfg['tag'] == 'setting':
        q.page['content_01'] = ui.section_card(box=ui.box(
            zone='content_0'), title='', subtitle='', items=page_cfg['save_buttons'])
        q.page['content_10'] = ui.form_card(box=ui.box(
            zone='content_1', width='40%', order=1), title='', items=page_cfg['setting_items'])
        q.page['content_11'] = ui.form_card(box=ui.box(
            zone='content_1', width='30%', order=2), title='', items=page_cfg['upload_items'])
        q.page['content_12'] = ui.form_card(box=ui.box(
            zone='content_1', width='30%', order=3), title='', items=page_cfg['color_picker_items'])

    elif page_cfg['tag'] == 'jd':
        q.page['content_00'] = page_cfg['jd_add_card']
        q.page['content_01'] = page_cfg['jd_table_card']
        q.page['content_10'] = page_cfg['jd_info_card']
        q.page['content_11'] = page_cfg['cv_list_card']

    elif page_cfg['tag'] == 'cv':
        q.page['content_00'] = page_cfg['jd_content_card']
        q.page['content_01'] = page_cfg['jd_skill_card']
        # q.page['content_02'] = page_cfg['jd_edu_card']
        # q.page['content_03'] = page_cfg['jd_exp_card']
        q.page['content_10'] = page_cfg['total_stat_card']
        q.page['content_18'] = page_cfg['similarity_stat_card']
        q.page['content_11'] = page_cfg['skill_stat_card']
        q.page['content_12'] = page_cfg['edu_stat_card']
        q.page['content_13'] = page_cfg['exp_stat_card']
        q.page['content_14'] = page_cfg['cv_content_card']
        q.page['content_15'] = page_cfg['cv_skill_card']
        q.page['content_16'] = page_cfg['cv_edu_card']
        q.page['content_17'] = page_cfg['cv_exp_card']

    await q.page.save()
