function resetFrez() {
    if (editMode && frezId) {
        resetChoise();
        btn = document.getElementById(btnId);
        btn.innerHTML = 'تعديل';

        let items1 = Array.prototype.slice.call(
            document.getElementsByClassName(frezId),
            0
        );
        $(`.${frezId}[data-toggle="datepicker"]`).datepicker('destroy');
        for (let i = 0; i < items1.length; i++) {
            items1[i].innerHTML = originals[items1[i].getAttribute('name')];
            items1[i].className = `editable ${frezId}`;
            items1[i].setAttribute('contenteditable', 'false');
        }
        editMode = false;
        frezId = '';
        btnId = '';
        originals = {};
    }
}

function editFrez(e, id, did) {
    if (editMode && frezId !== `fr-${id}`) {
        reset();
    }
    editMode = true;
    frezId = `fr-${id}`;
    btnId = `freb-${id}`;
    let items1 = Array.prototype.slice.call(
        document.getElementsByClassName(frezId),
        0
    );

    if (e.target.innerHTML === 'تعديل') {
        e.target.innerHTML = 'حفظ';
        $(`.${frezId}[data-toggle="datepicker"]`).datepicker({
            autoHide: true,
        });
        $('#keyTips').removeClass('d-none');

        for (let i = 0; i < items1.length; i++) {
            originals[items1[i].getAttribute('name')] = items1[i].innerHTML;
            items1[i].setAttribute('contenteditable', 'true');
            if (items1[i].classList.contains('mul')) {
                items1[
                    i
                ].className = `editable border border-dark rounded p-2 fr-${id} mul activee`;
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
                ].className = `editable border border-dark rounded p-2 fr-${id}`;
            }
        }
    } else if (e.target.innerHTML === 'حفظ') {
        const schema = {
            freezeDecisionDate: (str) => {
                return validator.isDate(str, { format: 'mm/dd/yyyy' });
            },
            freezeDecisionNumber: (str) => {
                return !validator.isEmpty(str) && validator.isNumeric(str);
            },
            freezeDecisionType: (str) => {
                return (
                    validator.equals(str, 's') ||
                    validator.equals(str, 'o') ||
                    validator.equals(str, 'b')
                );
            },
            freezeDurationYear: (str) => true,
            freezeDurationMonth: (str) => true,
            freezeDurationDay: (str) => true,
        };
        const errors = {
            freezeDecisionDate: 'تأكد من حقل تاريخ القرار',
            freezeDecisionNumber: 'تأكد من حقل رقم القرار',
            freezeDecisionType: 'تأكد من حقل نوع القرار',
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
                    items1[i].className = `editable fr-${id} mul`;
                } else {
                    items1[i].className = `editable fr-${id}`;
                }

                items1[i].setAttribute('contenteditable', 'false');
            }
            e.target.innerHTML = 'تعديل';
            $(`.${frezId}[data-toggle="datepicker"]`).datepicker('destroy');
            $('#keyTips').addClass('d-none');

            editMode = false;
            frezId = '';
            btnId = '';
            orignals = {};
            console.log(values);
            values['csrfmiddlewaretoken'] = csrf.value;

            edit(values, id, did, 'fr');
        } else {
            values = {};
        }
    }
}
