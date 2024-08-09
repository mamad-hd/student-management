from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Treeview
from bl.student_bl import create_student, edit_student, get_students, remove_student


def show_error(data: dict) -> None:
    err_list = []

    for field, err in data.items():
        err_list.append(f"Error({field})! {err}.")

    showerror("Error!!!", "\n".join(err_list))


def show_success(data: dict) -> None:
    succ_list = []

    for field, msg in data.items():
        succ_list.append(f"Success({field})! {msg}.")

    showinfo("Success!!!", "\n".join(succ_list))


def student_main_form():

    def load_student():
        result = get_students()

        if not result["SUCCESS"]:
            show_error(result["ERROR_MESSAGE"])
            return []
        else:
            return result["RETURN_DATA"]

    def add_btn_onclick():
        form.withdraw()
        student_data_entery_form(student_grid=student_grid)
        form.deiconify()

    def edit_btn_onclick():
        rows_id = student_grid.selection()

        if not rows_id:
            show_error({"row error": "selected error"})
            return

        if len(rows_id) > 1:
            show_error({"row error": "selected error"})
            return

        name, family, gender, age, phone, ncode, stdcode, python_score, java_score, c_score, description = student_grid.item(
            rows_id[0], "values")

        if askyesno("Warning!", f"Do you want to edit this student ?\n\nFullname: {name} {family}, Phone: {phone}, ncode: {ncode}, stdcode: {stdcode}"):

            form.withdraw()
            student_editing_form(row_id=rows_id[0],
                name=name,
                family=family,
                gender=gender,
                age=age,
                phone=phone,
                ncode=ncode,
                stdcode=stdcode,
                python_score=python_score,
                java_score=java_score,
                c_score=c_score,
                description=description,
                student_grid=student_grid
            )
            form.deiconify()

    def remove_btn_onclick():
        rows_id = student_grid.selection()

        if not rows_id:
            show_error({"row error": "selected error"})
            return

        for id_ in rows_id:
            name, family, gender, age, phone, ncode, stdcode, python_score, java_score, c_score, description = student_grid.item(id_, "values")

            if askyesno("Warning!", f"Do you want to delete this student ?\n\nFullname: {name} {family}, Phone: {phone}, ncode: {ncode}, stdcode: {stdcode}"):

                result = remove_student(phone=phone)

                if not result["SUCCESS"]:
                    show_error(result["ERROR_MESSAGE"])
                else:
                    student_grid.delete(id_)
                    show_success(result["SUCCESS_MESSAGE"])

    def exit_btn_onclick():
        form.destroy()

    student_list = load_student()

    form = Tk()

    # region config form
    form.title("student management system")

    app_icon = PhotoImage(file=r"images\app_icon.png")
    form.iconphoto(False, app_icon)

    form_width = 600
    form_height = 600
    padding_top = (form.winfo_screenheight()//2) - (form_height//2)
    padding_left = (form.winfo_screenwidth()//2) - (form_width//2)
    form.geometry(f"{form_width}x{form_height}+{padding_left}+{padding_top}")
    # form.resizable(width=False, height=False)
    form.configure(bg="white")
    # endregion

    # region frame

    header = Frame(master=form, height=70, bg="#ebebeb",
                   highlightthickness=1, highlightbackground="#afafaf")
    header.pack(side=TOP, fill=X)
    header.propagate(False)

    footer = Frame(master=form, height=70, bg="#ebebeb",
                   highlightthickness=1, highlightbackground="#afafaf")
    footer.pack(side=BOTTOM, fill=X)
    footer.propagate(False)

    body = Frame(master=form, height=70, bg="white",
                 highlightthickness=1, highlightbackground="#afafaf")
    body.pack(fill=BOTH, expand=True, padx=10, pady=10)
    body.propagate(False)

    # endregion

    # region form title
    title_icon = PhotoImage(file=r"images\title_icon.png")

    Label(
        master=header,
        text="  student main form",
        bg="#ebebeb",
        font=("tahoma", 12, "bold"),
        image=title_icon,
        compound=LEFT
    ).pack(side=LEFT, padx=10)

    # endregion

    # region button

    exit_icon = PhotoImage(file=r"images\exit_icon.png")
    Button(
        master=footer,
        text="Exit",
        bg="#212529",
        fg="white",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#1c1f23",
        activeforeground="white",
        image=exit_icon,
        compound=LEFT,
        command=exit_btn_onclick
    ).pack(side=LEFT, padx=10)

    add_icon = PhotoImage(file=r"images\add_icon.png")
    Button(
        master=footer,
        text="Add",
        bg="#198754",
        fg="white",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#157347",
        activeforeground="white",
        image=add_icon,
        compound=LEFT,
        command=add_btn_onclick
    ).pack(side=RIGHT, padx=(0, 10))

    edit_icon = PhotoImage(file=r"images\edit_icon.png")
    Button(
        master=footer,
        text="Edit",
        bg="#ffc107",
        fg="black",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#ffca2c",
        activeforeground="black",
        image=edit_icon,
        compound=LEFT,
        command=edit_btn_onclick
    ).pack(side=RIGHT, padx=(0, 10))

    delete_icon = PhotoImage(file=r"images\delete_icon.png")
    Button(
        master=footer,
        text="Delete",
        bg="#dc3545",
        fg="white",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#bb2d3b",
        activeforeground="white",
        image=delete_icon,
        compound=LEFT,
        command=remove_btn_onclick
    ).pack(side=RIGHT, padx=(0, 10))
    # endregion

    # region grid, , padx=10, pady=10

    grid_y_scrollbar = Scrollbar(master=body, orient="vertical")
    grid_x_scrollbar = Scrollbar(master=body, orient="horizontal")

    grid_y_scrollbar.pack(side=RIGHT, fill=Y)
    grid_x_scrollbar.pack(side="bottom", fill=X)

    student_grid = Treeview(master=body, columns=(
        "name", "family", "gender", "age", "phone", "ncode", "stdcode", "python_score", "java_score", "c_score", "description"), show="headings", selectmode="extended")
    col_width = student_grid.winfo_width()

    student_grid.heading(column="name", text="Fisrtname", anchor=CENTER)
    student_grid.heading(column="family", text="Lastname", anchor=CENTER)
    student_grid.heading(column="gender", text="Gender", anchor=CENTER)
    student_grid.heading(column="age", text="age", anchor=CENTER)
    student_grid.heading(column="phone", text="Phone number", anchor=CENTER)
    student_grid.heading(column="ncode", text="ncode", anchor=CENTER)
    student_grid.heading(column="stdcode", text="stdcode", anchor=CENTER)
    student_grid.heading(column="python_score", text="python score", anchor=CENTER)
    student_grid.heading(column="java_score", text="java score", anchor=CENTER)
    student_grid.heading(column="c_score", text="c score", anchor=CENTER)
    student_grid.heading(column="description",
                         text="DEscription", anchor=CENTER)

    student_grid.column(column="name", anchor=CENTER, width=col_width)
    student_grid.column(column="family", anchor=CENTER, width=col_width)
    student_grid.column(column="gender",  anchor=CENTER, width=col_width)
    student_grid.column(column="age",  anchor=CENTER, width=col_width)
    student_grid.column(column="phone",  anchor=CENTER, width=col_width)
    student_grid.column(column="ncode",  anchor=CENTER, width=col_width)
    student_grid.column(column="stdcode",  anchor=CENTER, width=col_width)
    student_grid.column(column="python_score",  anchor=CENTER, width=col_width)
    student_grid.column(column="java_score",  anchor=CENTER, width=col_width)
    student_grid.column(column="c_score",  anchor=CENTER, width=col_width)
    student_grid.column(column="description", anchor=CENTER, width=col_width)

    student_grid.pack(fill=BOTH, expand=True)

    student_grid.configure()

    student_grid.configure(yscrollcommand=grid_y_scrollbar.set, xscrollcommand=grid_x_scrollbar.set)
    grid_y_scrollbar["command"] = student_grid.yview
    grid_x_scrollbar["command"] = student_grid.xview

    # endregion

    # region grid dataentry
    for student in student_list:
        student_grid.insert("", END, values=(
            student['name'], student['family'], student['gender'], student['age'], student['phone'], student['ncode'], student['stdcode'], student['python_score'], student['java_score'], student['c_score'], student['description']))

    # endregion

    form .mainloop()


def student_data_entery_form(student_grid):

    def back_btn_onclick():
        form.quit()
        form.destroy()

    def add_btn_onclick():
        student = {
            "name": name_var.get(),
            "family": family_var.get(),
            "gender": gender_var.get(),
            "age": age_var.get(),
            "phone": phone_var.get(),
            "ncode": ncode_var.get(),
            "stdcode": stdcode_var.get(),
            "python_score": python_score_var.get(),
            "java_score": java_score_var.get(),
            "c_score": c_score_var.get(),
            "description": desc_entry.get("1.0", 'end-1c')
        }

        result = create_student(student=student)

        if not result["SUCCESS"]:

            if "name" in result["ERROR_MESSAGE"]:
                name_var.set("")

            if "family" in result["ERROR_MESSAGE"]:
                family_var.set("")

            if "gender" in result["ERROR_MESSAGE"]:
                gender_var.set("")

            if "age" in result["ERROR_MESSAGE"]:
                age_var.set("")

            if "phone" in result["ERROR_MESSAGE"]:
                phone_var.set("")

            if "ncode" in result["ERROR_MESSAGE"]:
                ncode_var.set("")

            if "stdcode" in result["ERROR_MESSAGE"]:
                stdcode_var.set("")

            if "python_scoer" in result["ERROR_MESSAGE"]:
                python_score_var.set("")

            if "java_scoer" in result["ERROR_MESSAGE"]:
                java_score_var.set("")

            if "c_scoer" in result["ERROR_MESSAGE"]:
                c_score_var.set("")

            if "description" in result["ERROR_MESSAGE"]:
                desc_entry.delete(1.0, "END")

            show_error(result["ERROR_MESSAGE"])

        else:
            student_grid.insert("", END, values=(
                student['name'], student['family'], student['gender'], student['age'], student['phone'], student['ncode'], student['stdcode'], student['python_score'], student['java_score'], student['c_score'], student['description']))
            show_success(result["SUCCESS_MESSAGE"])
            back_btn_onclick()

    form = Toplevel()

    # region variable
    name_var = StringVar()
    family_var = StringVar()
    gender_var = StringVar(value="male")
    age_var = StringVar()
    phone_var = StringVar()
    ncode_var = StringVar()
    stdcode_var = StringVar()
    python_score_var = StringVar()
    java_score_var = StringVar()
    c_score_var = StringVar()
    # endregion

    # region config form
    form.title("student management system")

    app_icon = PhotoImage(file=r"images\app_icon.png")
    form.iconphoto(False, app_icon)

    form_width = 600
    form_height = 600
    padding_top = (form.winfo_screenheight()//2) - (form_height//2)
    padding_left = (form.winfo_screenwidth()//2) - (form_width//2)
    form.geometry(f"{form_width}x{form_height}+{padding_left}+{padding_top}")
    # form.resizable(width=False, height=False)
    form.configure(bg="white")
    # endregion

    # region frame

    header = Frame(master=form, height=70, bg="#ebebeb",
                   highlightthickness=1, highlightbackground="#afafaf")
    header.pack(side=TOP, fill=X)
    header.propagate(False)

    footer = Frame(master=form, height=70, bg="#ebebeb",
                   highlightthickness=1, highlightbackground="#afafaf")
    footer.pack(side=BOTTOM, fill=X)
    footer.propagate(False)

    body = Frame(master=form, height=70, bg="white",
                 highlightthickness=1, highlightbackground="#afafaf")
    body.pack(fill=BOTH, expand=True, padx=10, pady=10)
    body.propagate(False)

    name_frame = Frame(master=body, height=28, bg="white")
    name_frame.pack(side=TOP, fill=X, pady=(10, 10), padx=10)
    name_frame.propagate(False)

    family_frame = Frame(master=body, height=28, bg="white")
    family_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    family_frame.propagate(False)

    gender_frame = Frame(master=body, height=28, bg="white")
    gender_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    gender_frame.propagate(False)

    age_frame = Frame(master=body, height=28, bg="white")
    age_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    age_frame.propagate(False)

    phone_frame = Frame(master=body, height=28, bg="white")
    phone_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    phone_frame.propagate(False)
    
    ncode_frame = Frame(master=body, height=28, bg="white")
    ncode_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    ncode_frame.propagate(False)

    stdcode_frame = Frame(master=body, height=28, bg="white")
    stdcode_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    stdcode_frame.propagate(False)

    python_score_frame = Frame(master=body, height=28, bg="white")
    python_score_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    python_score_frame.propagate(False)

    java_score_frame = Frame(master=body, height=28, bg="white")
    java_score_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    java_score_frame.propagate(False)

    c_score_frame = Frame(master=body, height=30, bg="white")
    c_score_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    c_score_frame.propagate(False)

    description_frame = Frame(master=body, height=28, bg="white")
    description_frame.pack(fill=BOTH, expand=True, pady=(0, 10), padx=10)
    description_frame.propagate(False)

    # endregion

    # region form title
    title_icon = PhotoImage(file=r"images\dataentry_icon.png")

    Label(
        master=header,
        text=" student data entry form",
        bg="#ebebeb",
        font=("tahoma", 12, "bold"),
        image=title_icon,
        compound=LEFT
    ).pack(side=LEFT, padx=10)

    # endregion

    # region button

    back_icon = PhotoImage(file=r"images\back_icon.png")
    Button(
        master=footer,
        text="Back",
        bg="#212529",
        fg="white",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#1c1f23",
        activeforeground="white",
        image=back_icon,
        compound=LEFT,
        command=back_btn_onclick
    ).pack(side=LEFT, padx=10)

    add_icon = PhotoImage(file=r"images\add_icon.png")
    Button(
        master=footer,
        text="Add",
        bg="#198754",
        fg="white",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#157347",
        activeforeground="white",
        image=add_icon,
        compound=LEFT,
        command=add_btn_onclick
    ).pack(side=RIGHT, padx=(0, 10))
    # endregion

    # region name
    Label(
        master=name_frame,
        text="First name : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=name_frame,
        textvariable=name_var,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal")
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region family
    Label(
        master=family_frame,
        text="Last name : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=family_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=family_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region gender
    Label(
        master=gender_frame,
        text="Gender : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Radiobutton(
        master=gender_frame,
        text="Male",
        variable=gender_var,
        value="male",
        bg="white"
    ).pack(side=LEFT)

    Radiobutton(
        master=gender_frame,
        text="Female",
        variable=gender_var,
        value="female",
        bg="white"
    ).pack(side=LEFT)

    Radiobutton(
        master=gender_frame,
        text="Other",
        variable=gender_var,
        value="other",
        bg="white"
    ).pack(side=LEFT)
    # endregion

    # region age
    Label(
        master=age_frame,
        text="Age : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=age_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=age_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region phone
    Label(
        master=phone_frame,
        text="Phone number : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=phone_frame,
        bg="#ededed",
        textvariable=phone_var,
        bd=1,
        font=("tahoma", 12, "normal")
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region ncode
    Label(
        master=ncode_frame,
        text="Ncode : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=ncode_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=ncode_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region stdcode
    Label(
        master=stdcode_frame,
        text="Stdcode : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=stdcode_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=stdcode_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region python_score
    Label(
        master=python_score_frame,
        text="Python score : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=python_score_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=python_score_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region java_score
    Label(
        master=java_score_frame,
        text="Java score : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=java_score_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=java_score_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region c_score
    Label(
        master=c_score_frame,
        text="C score : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=c_score_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=c_score_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region Description
    Label(
        master=description_frame,
        text="Description : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    desc_entry = Text(
        master=description_frame,
        bg="#ededed",
        bd=1,
    )
    desc_entry.pack(fill=BOTH, expand=True)

    # endregion

    form.mainloop()


def student_editing_form(row_id, name, family, gender, age, phone, ncode, stdcode, python_score, java_score, c_score, description, student_grid):

    def back_btn_onclick():
        form.quit()
        form.destroy()

    def edit_btn_onclick():

        student = {
            "name": name_var.get(),
            "family": family_var.get(),
            "gender": gender_var.get(),
            "age": age_var.get(),
            "phone": phone_var.get(),
            "ncode": ncode_var.get(),
            "stdcode": stdcode_var.get(),
            "python_score": python_score_var.get(),
            "java_score": java_score_var.get(),
            "c_score": c_score_var.get(),
            "description": desc_entry.get("1.0", 'end-1c')
        }

        result = edit_student(student=student)

        if not result["SUCCESS"]:

            if "name" in result["ERROR_MESSAGE"]:
                name_var.set("")

            if "family" in result["ERROR_MESSAGE"]:
                family_var.set("")

            if "gender" in result["ERROR_MESSAGE"]:
                gender_var.set("")

            if "age" in result["ERROR_MESSAGE"]:
                age_var.set("")

            if "phone" in result["ERROR_MESSAGE"]:
                phone_var.set("")

            if "ncode" in result["ERROR_MESSAGE"]:
                ncode_var.set("")

            if "stdcode" in result["ERROR_MESSAGE"]:
                stdcode_var.set("")

            if "python_score" in result["ERROR_MESSAGE"]:
                python_score_var.set("")

            if "java_score" in result["ERROR_MESSAGE"]:
                java_score_var.set("")

            if "c_score" in result["ERROR_MESSAGE"]:
                c_score_var.set("")

            if "description" in result["ERROR_MESSAGE"]:
                desc_entry.delete(1.0, "END")
                # desc_entry.insert("END", "")

            show_error(result["ERROR_MESSAGE"])

        else:
            student_grid.item(row_id, values=(
                student['name'], student['family'], student['gender'], student['age'], student['phone'], student['ncode'], student['stdcode'], student['python_score'], student['java_score'], student['c_score'], student['description']))
            show_success(result["SUCCESS_MESSAGE"])
            back_btn_onclick()

    form = Toplevel()

    # region variable
    name_var = StringVar(value=name)
    family_var = StringVar(value=family)
    gender_var = StringVar(value=gender)
    age_var = StringVar(value=age)
    phone_var = StringVar(value=phone)
    ncode_var = StringVar(value=ncode)
    stdcode_var = StringVar(value=stdcode)
    python_score_var = StringVar(value=python_score)
    java_score_var = StringVar(value=java_score)
    c_score_var = StringVar(value=c_score)
    # endregion

    # region config form
    form.title("student management system")

    app_icon = PhotoImage(file=r"images\app_icon.png")
    form.iconphoto(False, app_icon)

    form_width = 600
    form_height = 600
    padding_top = (form.winfo_screenheight()//2) - (form_height//2)
    padding_left = (form.winfo_screenwidth()//2) - (form_width//2)
    form.geometry(f"{form_width}x{form_height}+{padding_left}+{padding_top}")
    form.configure(bg="white")
    # endregion

    # region frame

    header = Frame(master=form, height=70, bg="#ebebeb",
                   highlightthickness=1, highlightbackground="#afafaf")
    header.pack(side=TOP, fill=X)
    header.propagate(False)

    footer = Frame(master=form, height=70, bg="#ebebeb",
                   highlightthickness=1, highlightbackground="#afafaf")
    footer.pack(side=BOTTOM, fill=X)
    footer.propagate(False)

    body = Frame(master=form, height=70, bg="white",
                 highlightthickness=1, highlightbackground="#afafaf")
    body.pack(fill=BOTH, expand=True, padx=10, pady=10)
    body.propagate(False)

    name_frame = Frame(master=body, height=28, bg="white")
    name_frame.pack(side=TOP, fill=X, pady=(10, 10), padx=10)
    name_frame.propagate(False)

    family_frame = Frame(master=body, height=28, bg="white")
    family_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    family_frame.propagate(False)

    gender_frame = Frame(master=body, height=28, bg="white")
    gender_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    gender_frame.propagate(False)

    age_frame = Frame(master=body, height=28, bg="white")
    age_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    age_frame.propagate(False)

    phone_frame = Frame(master=body, height=28, bg="white")
    phone_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    phone_frame.propagate(False)

    ncode_frame = Frame(master=body, height=28, bg="white")
    ncode_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    ncode_frame.propagate(False)

    stdcode_frame = Frame(master=body, height=28, bg="white")
    stdcode_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    stdcode_frame.propagate(False)

    python_score_frame = Frame(master=body, height=28, bg="white")
    python_score_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    python_score_frame.propagate(False)
    
    java_score_frame = Frame(master=body, height=28, bg="white")
    java_score_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    java_score_frame.propagate(False)

    c_score_frame = Frame(master=body, height=28, bg="white")
    c_score_frame.pack(side=TOP, fill=X, pady=(0, 10), padx=10)
    c_score_frame.propagate(False)

    description_frame = Frame(master=body, height=28, bg="white")
    description_frame.pack(fill=BOTH, expand=True, pady=(0, 10), padx=10)
    description_frame.propagate(False)

    # endregion

    # region form title
    title_icon = PhotoImage(file=r"images\dataentry_icon.png")

    Label(
        master=header,
        text=" student editing form",
        bg="#ebebeb",
        font=("tahoma", 12, "bold"),
        image=title_icon,
        compound=LEFT
    ).pack(side=LEFT, padx=10)

    # endregion

    # region button

    back_icon = PhotoImage(file=r"images\back_icon.png")
    Button(
        master=footer,
        text="Back",
        bg="#212529",
        fg="white",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#1c1f23",
        activeforeground="white",
        image=back_icon,
        compound=LEFT,
        command=back_btn_onclick
    ).pack(side=LEFT, padx=10)

    edit_icon = PhotoImage(file=r"images\edit_icon.png")
    Button(
        master=footer,
        text="Edit",
        bg="#ffc107",
        fg="black",
        padx=5,
        pady=10,
        font=("tahoma", 10, "bold"),
        activebackground="#ffca2c",
        activeforeground="black",
        image=edit_icon,
        compound=LEFT,
        command=edit_btn_onclick,
    ).pack(side=RIGHT, padx=(0, 10))
    # endregion

    # region name
    Label(
        master=name_frame,
        text="First name : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=name_frame,
        textvariable=name_var,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal")
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region family
    Label(
        master=family_frame,
        text="Last name : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=family_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=family_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region gender
    Label(
        master=gender_frame,
        text="Gender : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Radiobutton(
        master=gender_frame,
        text="Male",
        variable=gender_var,
        value="male",
        bg="white"
    ).pack(side=LEFT)

    Radiobutton(
        master=gender_frame,
        text="Female",
        variable=gender_var,
        value="female",
        bg="white"
    ).pack(side=LEFT)

    Radiobutton(
        master=gender_frame,
        text="Other",
        variable=gender_var,
        value="other",
        bg="white"
    ).pack(side=LEFT)
    # endregion

    # region age
    Label(
        master=age_frame,
        text="Age : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=age_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=age_var
    ).pack(fill=BOTH, expand=True)
    # endregion
    
    # region phone
    Label(
        master=phone_frame,
        text="Phone number : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=phone_frame,
        bg="#ededed",
        textvariable=phone_var,
        bd=1,
        font=("tahoma", 12, "normal"),
        state="disabled"
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region ncode
    Label(
        master=ncode_frame,
        text="Ncode : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=ncode_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=ncode_var,
        state="disabled"
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region stdcode
    Label(
        master=stdcode_frame,
        text="Stdcode : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=stdcode_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=stdcode_var,
        state="disabled"
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region python_score
    Label(
        master=python_score_frame,
        text="Python score : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=python_score_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=python_score_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region java_score
    Label(
        master=java_score_frame,
        text="Java score : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=java_score_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=java_score_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region c_score
    Label(
        master=c_score_frame,
        text="C score : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    Entry(
        master=c_score_frame,
        bg="#ededed",
        bd=1,
        font=("tahoma", 12, "normal"),
        textvariable=c_score_var
    ).pack(fill=BOTH, expand=True)
    # endregion

    # region Description
    Label(
        master=description_frame,
        text="Description : ",
        bg="white",
        fg="black",
        font=("tahoma", 10, "bold"),
        anchor=W,
        width=15
    ).pack(side=LEFT)

    desc_entry = Text(
        master=description_frame,
        bg="#ededed",
        bd=1
    )
    desc_entry.pack(fill=BOTH, expand=True)
    desc_entry.insert("end-1c", description)
    # endregion

    form .mainloop()
