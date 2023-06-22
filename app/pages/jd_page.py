
from h2o_wave import ui, Q
from .layout import render_template
from .utilities import *

async def jd_dialog(q: Q, details=None):
    dialog = ui.dialog(
            title='Add a Job Description',
            name='jd_upload',
            items=[
                ui.textbox(name='title', label='Job title'),
                ui.textbox(name='vacancies', label='Vacancies count'),
                ui.file_upload(name='jd_file', label='Upload', multiple=False, file_extensions=['txt'], compact=True),
                ui.button(name='submit_jd', label='Submit', primary=True)
            ],
            # Enable a close button (displayed at the top-right of the dialog)
            closable=True,
            # Get notified when the dialog is dismissed.
            events=['dismissed'],
        )
    q.page['meta'].dialog = dialog

async def jd_page(q, details=None):

    # Current job list
    jobs, vacancies = get_jobs(q)

    pic_card = ui.tall_info_card(
        box=ui.box(zone='content_0',
                order=0,
                #    height='',
                #    width='',
                ),
        name='add_jd',
        title='Job Positions',
        caption="available job roles",
        image=q.app.jd_image,
        image_height='420px',
        label='Add Job Role')
    
    # print('jobs > ', jobs, ' vacs > ', vacancies)
    jd_cards = [ui.inline([ui.persona(title=r, subtitle=f" Vacancies : {vacancies[i]}", size='s', name=r, image=q.app.jd_icon),
                            ui.button(name='select_job', label='view', icon='CaretRight8', value=r)], justify='between') for i,r in enumerate(jobs)]
    jd_table = ui.form_card(
        box=ui.box('content_0', 
                   order=1, 
                #    width='100%', 
                #    height='700px'
                   ),
        items=[
                # ui.button(name='add_jd', label='Add Job Description', primary=True, icon='CircleAdditionSolid', width='100%'),
               ui.text_m(content='Job Descriptions'),]+jd_cards,
    )

    # View JD
    try:
        selected_job = details['selected_job']
    except:
        selected_job = jobs[0]
    
    job_details = get_job_detail(q, selected_job)
    print("job details > ", job_details)
    q.user.job_data = job_details
    job_content = get_job_content(q, selected_job)
    # print("content > ", job_content)
    jd_details = ui.article_card(
        box=ui.box(zone='content_1',
                order=0,
                #    height='',
                #    width='',
                ),
        title=selected_job,
        content=job_content)

    # Selected CVs
    job_shortlist = get_job_shortlist(q, selected_job)
    # sample_cvs = ['001', '002', '003']
    cv_cards = [ui.inline([ui.persona(title=f"ID : {i}", subtitle=n, caption=f'Similarity Score : {s}', size='m', name=str(i), image=q.app.user_icon),
                            ui.button(name='view_cv', label='view', icon='NavigateExternalInline', value=str(i))], justify='between') for i,n,s in job_shortlist]
    cv_list = ui.form_card(
        box=ui.box('content_1', 
                   order=1, 
                #    width='100%', 
                #    height='700px'
                   ),
        items=[ui.text_m(content='Short Listed CVs'),]+cv_cards,
    )


    cfg = {
        'tag': 'jd',
        'jd_add_card': pic_card,
        'jd_table_card': jd_table,
        'jd_info_card': jd_details,
        'cv_list_card': cv_list,
    }
    await render_template(q, cfg)



