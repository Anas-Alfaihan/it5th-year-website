function resetEx() {
    if (editMode && exId) {
        resetChoise();
        btn = document.getElementById(btnId);
        btn.innerHTML = 'تعديل';

        let items1 = Array.prototype.slice.call(
            document.getElementsByClassName(exId),
            0
        );
        $(`.${exId}[data-toggle="datepicker"]`).datepicker('destroy');
        for (let i = 0; i < items1.length; i++) {
            items1[i].innerHTML = originals[items1[i].getAttribute('name')];
            items1[i].className = `editable ${exId}`;
            items1[i].setAttribute('contenteditable', 'false');
        }
        editMode = false;
        exId = '';
        btnId = '';
        originals = {};
    }
}

function editEx(e, id, did) {
    if (editMode && exId !== `ex-${id}`) {
        reset();
    }
    editMode = true;
    exId = `ex-${id}`;
    btnId = `exeb-${id}`;
    let items1 = Array.prototype.slice.call(
        document.getElementsByClassName(exId),
        0
    );

    if (e.target.innerHTML === 'تعديل') {
        e.target.innerHTML = 'حفظ';
        $(`.${exId}[data-toggle="datepicker"]`).datepicker({
            autoHide: true,
        });
        $('#keyTips').removeClass('d-none');

        for (let i = 0; i < items1.length; i++) {
            originals[items1[i].getAttribute('name')] = items1[i].innerHTML;
            items1[i].setAttribute('contenteditable', 'true');
            if (items1[i].classList.contains('mul')) {
                items1[
                    i
                ].className = `editable border border-dark rounded p-2 ex-${id} mul activee`;
                $(`.activee`).on({
                    focusin: function () {
                        $(
                            `~ .${items1[i].getAttribute('name')}`,
                            this
                        ).removeClass('d-none');
                        $(this).addClass('changeable');
                    },
                    blur: function () {
                        $(
                            `~ .${items1[i].getAttribute('name')}`,
                            this
                        ).addClass('d-none');
                        $(this).removeClass('changeable');
                    },
                });

                $(
                    `.activee + .${items1[i].getAttribute('name')} > div`
                ).mousedown(function () {
                    $(`.changeable`)
                        .text($('> strong', this).text())
                        .attr('value', $('> strong', this).attr('value'));
                });
            } else {
                items1[
                    i
                ].className = `editable border border-dark rounded p-2 ex-${id}`;
            }
        }
    } else if (e.target.innerHTML === 'حفظ') {
        const schema = {
            extensionDecisionDate: (str) => {
                return validator.isDate(str, { format: 'mm/dd/yyyy' });
            },
            extensionDecisionNumber: (str) => {
                return !validator.isEmpty(str) && validator.isNumeric(str);
            },
            extensionDecisionType: (str) => {
                return (
                    validator.equals(str, 's') ||
                    validator.equals(str, 'o') ||
                    validator.equals(str, 'b')
                );
            },
            extensionDurationYear: (str) => true,
            extensionDurationMonth: (str) => true,
            extensionDurationDay: (str) => true,
        };
        const errors = {
            extensionDecisionDate: 'تأكد من حقل تاريخ القرار',
            extensionDecisionNumber: 'تأكد من حقل رقم القرار',
            extensionDecisionType: 'تأكد من حقل نوع القرار',
        };

        let df = true;

        let values = {};
        for (let i = 0; i < items1.length; i++) {
            values[items1[i].getAttribute('name')] = items1[i].innerHTML;
            if (items1[i].hasAttribute('value')) {
                values[items1[i].getAttribute('name')] =
                    items1[i].getAttribute('value');
            }
            if (
                !schema[items1[i].getAttribute('name')](
                    values[items1[i].getAttribute('name')]
                )
            ) {
                df = false;
                window.alert(errors[items1[i].getAttribute('name')]);
                break;
            }
        }
        if (df) {
            for (let i = 0; i < items1.length; i++) {
                if (items1[i].classList.contains('mul')) {
                    items1[i].className = `editable ex-${id} mul`;
                } else {
                    items1[i].className = `editable ex-${id}`;
                }

                items1[i].setAttribute('contenteditable', 'false');
            }
            e.target.innerHTML = 'تعديل';
            $(`.${exId}[data-toggle="datepicker"]`).datepicker('destroy');
            $('#keyTips').addClass('d-none');

            editMode = false;
            exId = '';
            btnId = '';
            orignals = {};
            console.log(values);
            values['csrfmiddlewaretoken'] = csrf.value;

            edit(values, id, did, 'ex');
        } else {
            values = {};
        }
    }
}
