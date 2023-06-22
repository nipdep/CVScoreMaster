from h2o_wave import ui, site, data
from .layout import render_template

from .utilities import *

import random


async def launch_page(q, details=None):
    # === Info card ===
    profile_info_card = ui.profile_card(
        box=ui.box(zone='content_0', order=1, height='320px'),
        image="https://pbs.twimg.com/profile_images/1468640599871918083/MIKXVFJo_normal.jpg", # noqa
        persona=ui.persona(
            title="Title", #noqa
            subtitle="Lorem ipsum dolor sit amet, posidonium liberavisse id pro.", #noqa
            image="https://pbs.twimg.com/profile_images/1468640599871918083/MIKXVFJo_normal.jpg"), #noqa
        items=[]
    )

    # ===== Card-1 ======
    user_stats_card = ui.tall_stats_card(
        box=ui.box(zone='content_0', order=2, height='360px'),
        items=[
            ui.stat(label='Count - Lorem ipsum', value="11", icon='View', icon_color='blue'), #noqa
            ui.stat(label='Count - Lorem ipsum', value="10", icon='AddFriend', icon_color='green'), #noqa
            ui.stat(label='Count - Lorem ipsum', value="9", icon='Calories', icon_color='red'), #noqa
            ui.stat(label='Count - Lorem ipsum', value="14", icon='CategoryClassification', icon_color='blue'), #noqa
        ])

    # ===== Card-2 =====
    st_stat_card = ui.small_series_stat_card(
        box=ui.box(zone='content_1', order=1, width='285px'),
        title="stat - Lorem ipsum",
        value=str(100),
        plot_category='foo',
        plot_type='area',
        plot_value='qux',
        plot_color="#0078AA",
        plot_data=data(
            fields=['foo', 'qux'], 
            rows=list(zip(range(7), [3,12,45,23,5,23,5])), #noqa
            pack=True),
        plot_zero_value=0,
        plot_curve='step',
    )

    # ====== Card-3 =====
    rt_stat_card = ui.small_series_stat_card(
        box=ui.box(zone='content_1', order=2, width='285px'),
        title="stat - Lorem ipsum",
        value=str(34),
        plot_category='foo',
        plot_type='area',
        plot_value='qux',
        plot_color="#3AB4F2",
        plot_data=data(
            fields=['foo', 'qux'], 
            rows=list(zip(range(7), [31,12,45,23,15,23,5])),
            pack=True),
        plot_zero_value=0,
        plot_curve='step',
    )

    # ===== Card-4 ======
    like_stat_card = ui.small_series_stat_card(
        box=ui.box(zone='content_1', order=2, width='285px'),
        title="stat - Lorem ipsum",
        value=str(12),
        plot_category='foo',
        plot_type='area',
        plot_value='count',
        plot_color="#D61C4E",
        plot_data=data(
            fields=['days', 'count'], 
            rows=list(zip(range(7), [1,2,3,4,1,2,2])),
            pack=True),
        plot_zero_value=0,
        plot_curve='step',
    )

    # ===== Card-5 ======
    rp_stat_card = ui.small_series_stat_card(
        box=ui.box(zone='content_1', order=2, width='285px'),
        title="stat - Lorem ipsum",
        value=str(24),
        plot_type='area',
        plot_value='count',
        plot_color="#231955",
        plot_data=data(
            fields=['days','count'], 
            rows=list(zip(range(7), [2,10,1,7,8,1,5])),
            pack=True),
        plot_zero_value=0,
        plot_curve='step',
    )

    # ===== Fill Card ======
    filter_card = ui.form_card(
        box=ui.box(zone='content_2', order=0, width='100%'),
        items=[]
    )
    

    cfg = {
        'tag': 'launch',
        'user_info_card': profile_info_card,
        'user_st_card': user_stats_card,
        'weekly_st_stats': st_stat_card,
        'weekly_rt_stats': rt_stat_card,
        'weekly_like_stats': like_stat_card,
        'weekly_rp_stats': rp_stat_card,
        'filter_card': filter_card,
    }
    await render_template(q, cfg)