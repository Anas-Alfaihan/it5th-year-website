function resetDemon() {
  if (editMode && demonId) {
    resetChoise();
    btn = document.getElementById(btnId);
    btn.innerHTML = "تعديل";

    let items1 = Array.prototype.slice.call(document.getElementsByClassName(demonId), 0);
    $(`.${demonId}[data-toggle="datepicker"]`).datepicker("destroy");
    for (let i = 0; i < items1.length; i++) {
      items1[i].innerHTML = originals[items1[i].getAttribute("name")];
      items1[i].className = `editable ${demonId}`;
      items1[i].setAttribute("contenteditable", "false");
    }
    editMode = false;
    exId = "";
    btnId = "";
    originals = {};
  }
}

function editDemon(e, id) {
  if (editMode && demonId !== `demon-${id}`) {
    reset();
  }
  editMode = true;
  demonId = `demon-${id}`;
  btnId = `deb-${id}`;
  let items1 = Array.prototype.slice.call(document.getElementsByClassName(demonId), 0);

  if (e.target.innerHTML === "تعديل") {
    e.target.innerHTML = "حفظ";
    $(`.${demonId}[data-toggle="datepicker"]`).datepicker({
      autoHide: true,
    });
    $("#keyTips").removeClass("d-none");

    for (let i = 0; i < items1.length; i++) {
      originals[items1[i].getAttribute("name")] = items1[i].innerHTML;
      items1[i].setAttribute("contenteditable", "true");
      if (items1[i].classList.contains("mul")) {
        items1[i].className = `editable border border-dark rounded p-2 demon-${id} mul activee`;
        $(`.activee`).on({
          focusin: function () {
            $(`~ .${items1[i].getAttribute("name")}`, this).removeClass("d-none");
            $(this).addClass("changeable");
          },
          blur: function () {
            $(`~ .${items1[i].getAttribute("name")}`, this).addClass("d-none");
            $(this).removeClass("changeable");
          },
        });

        $(`.activee + .${items1[i].getAttribute("name")} > div`).mousedown(function () {
          $(`.changeable`).text($("> strong", this).text()).attr("value", $("> strong", this).attr("value"));
        });
      } else {
        items1[i].className = `editable border border-dark rounded p-2 demon-${id}`;
      }
    }
  } else if (e.target.innerHTML === "حفظ") {
    const schema = {
      name: (str) => {
        return !validator.isEmpty(str);
      },
      fatherName: (str) => {
        return !validator.isEmpty(str);
      },
      motherName: (str) => {
        return !validator.isEmpty(str);
      },
      home: (str) => {
        return !validator.isEmpty(str);
      },
      residence: (str) => {
        return !validator.isEmpty(str);
      },
      mobile: (str) => {
        return !validator.isEmpty(str);
      },
      telephone: (str) => {
        return !validator.isEmpty(str);
      },
      email: (str) => {
        return validator.isEmail(str);
      },
      birthDate: (str) => {
        return validator.isDate(str, { format: "mm/dd/yyyy" });
      },
      gender: (str) => {
        return validator.equals(str, "male") || validator.equals(str, "female");
      },
      currentAdjective: (str) => {
        return validator.equals(str, "demonstrator") || validator.equals(str, "returning") || validator.equals(str, "envoy") || validator.equals(str, "returning demonstrator") || validator.equals(str, "loathes") || validator.equals(str, "transfer outside the university") || validator.equals(str, "end services") || validator.equals(str, "resigned");
      },
      maritalStatus: (str) => {
        return validator.equals(str, "married") || validator.equals(str, "unmarried");
      },
      militarySituation: (str) => {
        return validator.equals(str, "delayed") || validator.equals(str, "laid off");
      },
      university: (str) => {
        return !validator.isEmpty(str);
      },
      college: (str) => {
        return !validator.isEmpty(str);
      },
      section: (str) => {
        return true;
      },
      specialization: (str) => {
        return true;
      },
      commencementAfterNominationDate: (str) => {
        return validator.isEmpty(str) || validator.isDate(str, { format: "mm/dd/yyyy" });
      },
      language: (str) => {
        return !validator.isEmpty(str);
      },
    };
    const errors = {
      name: "تأكد من حقل الاسم",
      fatherName: "تأكد من حقل اسم الأب",
      motherName: "تأكد من حقل اسم الأم",
      home: "تأكد من حقل مكان الإقامة",
      residence: "تأكد من حقل العنوان الحالي",
      mobile: "تأكد من رقم الهاتف المحمول",
      telephone: "تأكد من رقم الهاتف الأرضي",
      email: "تأكد من الإيميل",
      birthDate: "تأكد من تاريخ الولادة",
      currentAdjective: "تأكد من حقل الصفة الحالية",
      gender: "تأكد من حقل الجنس",
      maritalStatus: "تأكد من حقل الحالة الاجتماعية",
      militarySituation: "تأكد من حقل الوضع العسكري",
      university: "تأكد من حقل جامعة التعيين",
      college: "تأكد من حقل كلية التعيين",
      commencementAfterNominationDate: "تأكد من حقل المباشرة ",
      language: "تأكد من حقل اللغة",
    };

    let df = true;

    let values = {};
    for (let i = 0; i < items1.length; i++) {
      values[items1[i].getAttribute("name")] = items1[i].innerHTML;

      if (items1[i].hasAttribute("value")) {
        values[items1[i].getAttribute("name")] = items1[i].getAttribute("value");
      }
      if (!schema[items1[i].getAttribute("name")](values[items1[i].getAttribute("name")])) {
        df = false;
        window.alert(errors[items1[i].getAttribute("name")]);
        break;
      }
    }
    if (df) {
      for (let i = 0; i < items1.length; i++) {
        if (items1[i].classList.contains("mul")) {
          items1[i].className = `editable demon-${id} mul`;
        } else {
          items1[i].className = `editable demon-${id}`;
        }

        items1[i].setAttribute("contenteditable", "false");
      }
      $("#keyTips").addClass("d-none");
      e.target.innerHTML = "تعديل";
      $(`.${demonId}[data-toggle="datepicker"]`).datepicker("destroy");
      editMode = false;
      demonId = "";
      btnId = "";
      orignals = {};
      console.log(values);
      values["csrfmiddlewaretoken"] = csrf.value;

      edit(values, id, 9, "demon");
    } else {
      values = {};
    }
  }
}
