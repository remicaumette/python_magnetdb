from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse

from ..config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
@router.get("/index.html", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/api.html", response_class=HTMLResponse)
def api(request: Request):
    return templates.TemplateResponse('api.html', {"request": request})


@router.get("/dev.html", response_class=HTMLResponse)
def dev(request: Request):
    return templates.TemplateResponse('dev.html', {"request": request})

@router.get("/submit/{id}", response_class=HTMLResponse, name="submit")
@router.post("/submit/{id}", response_class=HTMLResponse, name="submit")
def submit(request: Request, id: int):
    return
    # with Session(engine) as session:
    #     material = session.get(Material, id)
    #     # print("update: input", material)
    #
        # form = forms.MaterialForm(obj=material)
        # form.name(disabled=True)
        # if form.validate_on_submit():
        #     # print("Material update validated")
        #     flash('Material has been updated')
        #
        #     # shall get MaterialBaseForm from form
        #     form.populate_obj(material)
        #     print("update output:", material)
        #     session.commit()
        #     session.refresh(material)
        #     return redirect(url_for('urls.index'))
        # else:
        #     # print("Material update not validated")
        #     flash('Material has been not updated:\n%s\n' %str(form.errors))
        #     #print("errors:", form.errors)

    # return render_template('submit.html', form=form, id=id)
