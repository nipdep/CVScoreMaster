
from h2o_wave import ui, Q
from .layout import render_template
from .utilities import *

async def cv_page(q: Q, details=None):

    # == JD ==
    # jd view
    # job_details = q.user.job_data
    jd_details_card = ui.tall_info_card(
        box=ui.box(zone='content_0',
                order=0,
                #    height='',
                #    width='',
                ),
        name='cv_back',
        title=q.user.job_data['job'],
        caption=q.user.job_data['content'],
        image=q.app.jd_ill,
        image_height='160px',
        label='Back')
    
    # JD skill list 
    meta_n = 3
    print("job_data > ", q.user.job_data)
    job_skills = eval(q.user.job_data['skills']) if isinstance(q.user.job_data['skills'], str) else q.user.job_data['skills']
    job_edu = q.user.job_data['education'] if isinstance(q.user.job_data['education'], str) else "No Explicit Requirement"
    job_exp = q.user.job_data['experience'] if isinstance(q.user.job_data['experience'], str) else "No Explicit Requirement"
    job_buttons = [ 
                ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%', icon='DeveloperTools', primary=False) for m in job_skills[i:i + meta_n]], width='100%')
                for i in range(0, len(job_skills), meta_n)
            ]
    jd_extracts_card = ui.form_card(
        box=ui.box(zone='content_0',
                   order=1,
                #    height='',
                #    width=''
                   ),
        items=[
            ui.text_m(content='Required Skills'),]+
            job_buttons+[
            ui.text_m(content='Required Education Level'),
            ui.button(name=job_edu, label=job_edu, disabled=True, visible=True, icon='Education', primary=False),
            ui.text_m(content='Required Experience Level'),
            ui.button(name=job_exp, label=job_exp, disabled=True, visible=True, icon='AddWork', primary=False),
            ui.textbox(name='job_title', label='whatever', disabled=True, visible=False, value=q.user.job_data['job'])
        ]
    )

    # == CV == 
    cv_details = get_cv_details(q, details['selected_cv'])
    print("cv details > ", cv_details)
    # CV Total score 
    total_score_card = ui.wide_gauge_stat_card (
        box=ui.box(zone='content_1',
                   order=0,
                #    width='',
                #    height=''
                   ),
        title='Total Score',
        value='={{intl foo minimum_fraction_digits=2 maximum_fraction_digits=2}}%',
        aux_value='',
        plot_color='$red',
        progress=float(cv_details['total_score']),
        data=dict(foo=f"{cv_details['total_score']*100:.2f}"),
    )

    # CV Similarity score
    similarity_score_card = ui.wide_gauge_stat_card (
        box=ui.box(zone='content_1',
                   order=0,
                #    width='',
                #    height=''
                   ),
        title='Similarity Score',
        value='={{intl foo minimum_fraction_digits=2 maximum_fraction_digits=2}}%',
        aux_value='',
        plot_color='$yellow',
        progress=float(cv_details['similarity_score']),
        data=dict(foo=f"{cv_details['similarity_score']*100:.2f}"),
    )

    # CV Skill score
    skill_score_card = ui.wide_bar_stat_card(
        box=ui.box(zone='content_2',
                   order=1,
                #    width='',
                #    height=''
                   ),
        title='Skill Score',
        value='={{intl foo minimum_fraction_digits=2 maximum_fraction_digits=2}}%',
        aux_value='',
        plot_color='$blue',
        progress=float(cv_details['skill_score']),
        data=dict(foo=f"{cv_details['skill_score']*100:.2f}"),
    )

    # CV Experience score 
    exp_score_card = ui.wide_bar_stat_card(
        box=ui.box(zone='content_2',
                   order=1,
                #    width='',
                #    height=''
                   ),
        title='Experience Score',
        value='={{intl foo minimum_fraction_digits=2 maximum_fraction_digits=2}}%',
        aux_value='',
        plot_color='$purple',
        progress=float(cv_details['exp_score']),
        data=dict(foo=f"{cv_details['exp_score']*100:.2f}"),
    )

    # CV Education score 
    edu_score_card = ui.wide_bar_stat_card(
        box=ui.box(zone='content_2',
                   order=1,
                #    width='',
                #    height=''
                   ),
        title='Education Score',
        value='={{intl foo minimum_fraction_digits=2 maximum_fraction_digits=2}}%',
        aux_value='',
        plot_color='$green',
        progress=float(cv_details['edu_score']),
        data=dict(foo=f"{cv_details['edu_score']*100:.2f}"),
    )

    # CV content 
    cv_details_card = ui.form_card(
        box=ui.box(zone='content_3',
                order=2,
                #    height='',
                #    width='',
                ),
        items=[
            ui.text_xl(content=f"ID : {cv_details['id']} | Name : {cv_details['name']}"),
            ui.text_l("Personal Details"),
            ui.text_m(cv_details['personal-content']),
            ui.text_l("Skill Details"),
            ui.text_m(cv_details['skill-content']),
            ui.text_l("Education Details"),
            ui.text_m(cv_details['education-content']),
            ui.text_l("Work Experience Details"),
            ui.text_m(cv_details['exp-content']),
        ]
        )
    
    # CV skill list 
    meta_n = 5
    skills = eval(cv_details['skills'])
    skill_buttons = [ 
                ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%', icon='DeveloperTools') for m in skills[i:i + meta_n]], width='100%')
                for i in range(0, len(skills), meta_n)
            ]
    cv_skills_card = ui.form_card(
        box=ui.box(zone='content_3',
                   order=2,
                   size='100%'
                #    height='',
                #    width=''
                   ),
        items=[
            ui.text_m(content='Skills'),
        ]+skill_buttons
    )

    # CV education level 
    edu = cv_details['education'] if isinstance(cv_details['education'], str) else "Haven't Mentioned"
    cv_edu_card = ui.form_card(
        box=ui.box(zone='content_3',
                   order=2,
                   size='100%'
                #    height='',
                #    width=''
                   ),
        items=[
            ui.text_m(content='Education Level'),
            ui.button(name=edu, label=edu, disabled=True, visible=True, icon='Education')
        ]
    )

    # CV experience level 
    exp = ["No Experience"] if eval(cv_details['experience']) == [] else eval(cv_details['experience']) 
    cv_exp_card = ui.form_card(
        box=ui.box(zone='content_3',
                   order=3,
                #    height='',
                #    width=''
                   ),
        items=[
            ui.text_m(content='Experience in months'),
            ui.buttons(items=[
                ui.button(name=i, label=i, disabled=True, visible=True, icon='AddWork') for i in exp
            ]),
        ]
    )

    cfg = {
        'tag': 'cv',
        'jd_content_card': jd_details_card,
        'jd_skill_card': jd_extracts_card,
        # 'jd_edu_card': jd_edu,
        # 'jd_exp_card': jd_exp,
        'cv_content_card': cv_details_card,
        'total_stat_card': total_score_card,
        'similarity_stat_card': similarity_score_card,
        'skill_stat_card': skill_score_card,
        'edu_stat_card': edu_score_card,
        'exp_stat_card': exp_score_card,
        'cv_skill_card': cv_skills_card,
        'cv_edu_card': cv_edu_card,
        'cv_exp_card': cv_exp_card,
    }
    await render_template(q, cfg)


