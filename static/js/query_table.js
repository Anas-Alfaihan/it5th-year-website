const templater = document.createElement('template');
templater.innerHTML = `
<style>
@import "/static/bootstrap-5.2.0/dist/css/bootstrap.rtl.min.css";
@import "/static/fontawesome-free-6.2.1-web/css/all.css";

    * {
        box-sizing: border-box;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
    }

    body {
        -webkit-font-smoothing: antialiased;
    }

    /* Table Styles */

    .ss {
        -webkit-user-select: none;

        -moz-user-select: none;

        -ms-user-select: none;

        user-select: none;
        cursor: grabbing !important;


    }

    .table-wrappe {
        margin: 10px 70px 70px;
        box-shadow: 0px 35px 50px rgba(0, 0, 0, 0.2);
        overflow-x: auto;
        cursor: grab;



    }

    .fl-table {
        border-radius: 5px;
        font-size: 18px;
        font-weight: normal;
        border: none;
        border-collapse: collapse;
        width: 100%;
        max-width: 100%;
        white-space: nowrap;
        background-color: white;
    }

    .fl-table td,
    .fl-table th {
        text-align: center;
        padding: 8px;
        max-width: 400px;
        overflow: auto;
    }
    .fl-table td:first-of-type,
    .fl-table th:first-of-type {
        text-align: center;
        padding: 8px;
        min-width: 30px;
    }

    .fl-table td {
        border-right: 1px solid #f8f8f8;
        font-size: 16px;
        border: 1px solid rgb(247, 245, 245)

    }

    .fl-table thead th {
        color: #ffffff;
        background: #324960;
    }


    .fl-table thead th:nth-child(odd) {
        color: #ffffff;
        background: #324960;
    }

    .fl-table tr:nth-child(even) {
        background: #F8F8F8;
    }

    .td-table>table {
        padding: 10px;
    }

    .td-table th {
        color: #ffffff;
        background: #53779b !important;
    }

    /* Responsive */
    @media print {
        .table-wrappe {
            position: fixed;
            top: 0px;
            right: 0px;
            margin: 0;
        }
    }

    @media (max-width: 767px),
    print {
        .fl-table {
            display: block;
            width: 100%;
        }

        .table-wrappe:before {
            display: block;
            text-align: left;
            font-size: 11px;
            color: white;
            padding: 0 0 10px;
        }

        .fl-table thead,
        .fl-table tbody,
        .fl-table thead th {
            display: block;
        }

        .fl-table thead th:last-child {
            border-bottom: none;
        }

        .fl-table thead {
            float: right;
        }

        .fl-table tbody {
            width: auto;
            position: relative;
            overflow-x: auto;
        }

        .fl-table td,
        .fl-table th {
            padding: 20px .625em .625em .625em;
            height: 60px;
            vertical-align: middle;
            box-sizing: border-box;
            overflow-x: hidden;
            overflow-y: auto;
            max-width: 120px;
            font-size: 13px;
            text-overflow: ellipsis;
            
        }

        .fl-table thead th {
            text-align: right;
            border-bottom: 1px solid #f7f7f9;
        }

        .fl-table tbody tr {
            display: table-cell;
        }

        .fl-table tbody tr:nth-child(odd) {
            background: none;
        }

        .fl-table tr:nth-child(even) {
            background: transparent;
        }

        .fl-table tr td:nth-child(odd) {
            background: #F8F8F8;
            border-left: 1px solid #E6E4E4;
        }

        .fl-table tr td:nth-child(even) {
            border-left: 1px solid #E6E4E4;
        }

        .fl-table tbody td {
            display: block;
            text-align: center;
        }
    }
</style>
<script>

    const slider = document.querySelector('.table-wrappe');
    let isDown = false;
    let startX;
    let scrollLeft;

    slider.addEventListener('mousedown', (e) => {
        isDown = true;

        slider.classList.add('ss');

        slider.classList.add('active');
        slider.classList.add('active');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });
    slider.addEventListener('mouseleave', () => {
        isDown = false;
        slider.classList.remove('active');
        slider.classList.remove('ss');

    });
    slider.addEventListener('mouseup', () => {
        isDown = false;
        slider.classList.remove('active');
        slider.classList.remove('ss');
    });
    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 3; //scroll-fast
        slider.scrollLeft = scrollLeft - walk;
        console.log(walk);
    });

</script>
`;

class DataTabler extends HTMLElement {
    constructor() {
        super();

        if (this.hasAttribute('src')) this.src = this.getAttribute('src');
        // If no source, do nothing
        if (!this.src) return;

        // attributes to do, datakey
        if (this.hasAttribute('cols'))
            this.cols = this.getAttribute('cols').split(',');

        // helper values for sorting and paging
        this.sortAsc = false;
        this.df = [];
        this.levelOne = {
            name: 'الاسم',
            fatherName: 'اسم الأب',
            motherName: 'اسم الأم',
            gender: 'الجنس',
            birthDate: 'تاريخ الميلاد',
            email: 'الإيميل',
            telephone: 'رقم الهاتف الإرضي',
            maritalStatus: 'الوضع الاجتماعي',
            militarySituation: 'الوضع العسكري',
            email: 'الإيميل',
            language: 'اللغة',
            currentAdjective: 'الصفة الحالية',
            nominationReason: 'سبب الترشيح',
            contestAnnouncementDate: 'تاريخ المسابقة',
            university: 'الجامعة',
            college: 'الكلية',
            section: 'القسم',
            'universityDegree.universityDegreeUniversity': 'جامعة التخرج',
            'universityDegree.universityDegreeCollege': 'كلية التخرج',
            'universityDegree.universityDegreeSection': 'قسم التخرج',
            'universityDegree.universityDegreeYear': 'سنة التخرج',
            'universityDegree.universityDegreeAverage': 'معدل التخرج',
            specialization: 'التخصص',
            'nominationDecision.nominationDecisionNumber': 'رقم قرار الترشيح',
            'nominationDecision.nominationDecisionType': 'نوع قرار الترشيح',
            'nominationDecision.nominationDecisionDate': 'تاريخ قرار الترشيح',
            commencementAfterNominationDate: 'تاريخ المباشرة',
            residence: 'العنوان الحالي',
            mobile: 'رقم الهاتف المحمول',
            home: 'عنوان اﻹقامة',
        };
        this.levelTwo = {
            dispatch: 'إيفاد',
            certificateOfExcellence: 'شهادة التفوق',
            graduateStudies: 'دراسات عليا',
        };
        this.levelThree = {
            freeze: 'freeze',
            extension: 'extension',
        };

        this.op = {
            gender: {
                male: 'ذكر',
                female: 'أنثى',
            },
            maritalStatus: {
                married: 'متزوج',
                unmarried: 'أعزب',
            },
            militarySituation: {
                delayed: 'مؤجل',
                'laid off': 'مسرح',
            },
            currentAdjective: {
                demonstrator: 'معيد',
                returning: 'عائد',
                envoy: 'موفد',
                'returning demonstrator': 'معيد عائد',
                loathes: 'مستنكف',
                'transfer outside the university': 'نقل خارج الجامعة',
                'end services': 'انهاء خدمات',
                resigned: 'انهاء بحكم المستقيل',
            },
            nominationReason: {
                contest: 'مسابقة',
                'First graduate': 'خريج أول',
            },
            'nominationDecision.nominationDecisionType': {
                s: 'ش.ع',
                o: 'و',
                b: 'ب',
            },
        };
        const shadow = this.attachShadow({
            mode: 'open',
        });
        this.shadowRoot.appendChild(templater.content.cloneNode(true));
        const div1 = document.createElement('div');
        const table = document.createElement('table');
        table.classList.add('fl-table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        tbody.classList.add('table-group-divider');

        table.append(thead, tbody);

        (this.cer = false), (this.dis = false), (this.grad = false);

        const nav = document.createElement('div');
        nav.classList.add('px-3');

        const exportbtn = document.createElement('button');
        exportbtn.classList.add('btn', 'btn-outline-primary', 'mx-2');
        exportbtn.innerHTML = 'تصدير';
        nav.append(exportbtn);

        div1.append(table);
        div1.classList.add('table-wrappe');

        shadow.append(div1, nav);

        // Attach the created elements to the shadow dom

        // https://www.freecodecamp.org/news/this-is-why-we-need-to-bind-event-handlers-in-class-components-in-react-f7ea1a6f93eb/
        this.sort = this.sort.bind(this);
        this.printable = [];

        this.exportbtn = this.exportbtn.bind(this);

        exportbtn.addEventListener('click', this.exportbtn, false);
    }

    exportbtn() {
        let objArray = [];

        this.printable.forEach((o) => {
            objArray.push(o.join(','));
        });

        const blob = new Blob([objArray.join('\r\n')], { type: 'text/csv' });

        // Creating an object for downloading url
        const url = window.URL.createObjectURL(blob);

        // Creating an anchor(a) tag of HTML
        const a = document.createElement('a');

        // Passing the blob downloading url
        a.setAttribute('href', url);

        // Setting the anchor tag attribute for downloading
        // and passing the download file name
        a.setAttribute('download', 'download.csv');

        // Performing a download with click
        a.click();
    }

    load() {
        // error handling needs to be done :|

        let y = JSON.parse(this.src);

        this.data = y['data'];
        console.log(this.data);
        console.log(this.cols);
        this.df = this.data;
        this.render();
    }

    render() {
        if (!this.cols) this.cols = Object.keys(this.data[0]);

        this.renderHeader();
        this.renderBody();
    }

    renderBody() {
        let result = '';
        let counter = 1;
        this.data.forEach((c) => {
            let r = `<tr>`;
            r += `<td>${counter}</td>`;
            counter++;
            let h = [];
            let ob = [];

            this.cols.forEach((col) => {
                if (_.has(this.levelOne, col)) {
                    if (_.has(this.op, col)) {
                        r += `<td>${
                            this.op[col][_.get(c, col)]
                                ? this.op[col][_.get(c, col)]
                                : ''
                        }</td>`;
                        ob.push(
                            this.op[col][_.get(c, col)]
                                ? this.op[col][_.get(c, col)]
                                : ''
                        );
                    } else {
                        r += `<td>${_.get(c, col) ? _.get(c, col) : ''}</td>`;
                        ob.push(_.get(c, col) ? _.get(c, col) : '');
                    }

                    h.push(this.levelOne[col]);
                }
            });
            if (this.cer) {
                r += `<td>${this.renderCer(c['certificateOfExcellence'])}</td>`;
                ob.push(
                    _.replace(
                        this.renderCer(c['certificateOfExcellence']),
                        /<br\/>/g,
                        ''
                    )
                );
                h.push(this.levelTwo['certificateOfExcellence']);
            }
            if (this.grad) {
                r += `<td>${this.renderGrad(c['graduateStudies'])}</td>`;
                ob.push(
                    _.replace(this.renderGrad(c['graduateStudies'])),
                    /<br\/>/g,
                    ''
                );
                h.push(this.levelTwo['graduateStudies']);
            }
            if (this.dis) {
                r += `<td dir="auto" style="unicode-bidi: embed;display: flex;justify-content: space-between; flex-direction: column">${this.renderDis(
                    c['dispatch']
                )}</td>`;
                ob.push(
                    _.replace(this.renderDis(c['dispatch'])),
                    /<br\/>/g,
                    ''
                );
                h.push(this.levelTwo['dispatch']);
            }
            if (this.printable.length === 0) {
                this.printable.push(h);
            }
            this.printable.push(ob);
            r += '</tr>';
            result += r;
        });

        let tbody = this.shadowRoot.querySelector('tbody');
        tbody.innerHTML = result;
    }

    renderDis(l) {
        let s = '';
        l.forEach((c) => {
            s += `<span style="display: flex; justify-content: space-between"><span>${c.requiredCertificate}</span> | <span>${c.alimony}</span> | <span>${c.dispatchCountry}</span> | <span>${c.dispatchDecisionNumber}\\${c.dispatchDecisionType}</span>  | <span>${c.dispatchDecisionDate}</span> | <span>${c.dispatchDurationDay}-${c.dispatchDurationMonth}-${c.dispatchDurationYear}</span>`;
            s += '</span>';
        });
        return s;
    }

    renderCer(l) {
        let s = '';
        l.forEach((c) => {
            s += `شهادة تفوق بدرجة ${c.certificateOfExcellenceDegree} في السنة ${c.certificateOfExcellenceYear}`;
            s += '<br/>';
        });
        return s;
    }
    renderGrad(l) {
        let s = '';
        l.forEach((g) => {
            s += `شهادة ${g.graduateStudiesDegree} من جامعة ${g.graduateStudiesUniversity} كلية ${g.graduateStudiesCollege} قسم ${g.graduateStudiesSection} تخصص ${g.graduateStudiesSpecialzaion} بمعدل ${g.graduateStudiesAverage} سنة ${g.graduateStudiesYear}`;
            s += '<br/>';
        });
        return s;
    }

    renderHeader() {
        let header = '<tr>';
        header += `<th scope='col' data-sort="id">#</th>`;

        this.cols.forEach((c) => {
            if (c !== 'id' && _.has(this.levelOne, c))
                header += `<th scope='col' data-sort="${c}">${this.levelOne[c]} </th>`;
            else if (
                _.has(this.levelTwo, `certificateOfExcellence`) &&
                !this.cer
            ) {
                this.cer = true;
                header += `<th scope='col' >${this.levelTwo['certificateOfExcellence']} </th>`;
            } else if (_.has(this.levelTwo, `graduateStudies`) && !this.grad) {
                this.grad = true;
                header += `<th scope='col' >${this.levelTwo['graduateStudies']} </th>`;
            } else if (_.has(this.levelTwo, `dispatch`) && !this.dis) {
                this.dis = true;
                header += `<th scope='col' >${this.levelTwo['dispatch']} </th>`;
            }
        });

        header += '</tr>';
        let thead = this.shadowRoot.querySelector('thead');
        thead.innerHTML = header;

        this.shadowRoot.querySelectorAll('thead tr th').forEach((t) => {
            t.addEventListener('click', this.sort, false);
        });
    }

    async sort(e) {
        let thisSort = e.target.dataset.sort;

        if (this.sortCol && this.sortCol === thisSort)
            this.sortAsc = !this.sortAsc;
        this.sortCol = thisSort;
        if (this.sortCol === 'id') {
            this.data.sort((a, b) => {
                if (a['pk'] < b['pk']) return this.sortAsc ? 1 : -1;
                if (a['pk'] > b['pk']) return this.sortAsc ? -1 : 1;
                return 0;
            });
        } else {
            this.data.sort((a, b) => {
                if (a[this.sortCol] < b[this.sortCol])
                    return this.sortAsc ? 1 : -1;
                if (a[this.sortCol] > b[this.sortCol])
                    return this.sortAsc ? -1 : 1;
                return 0;
            });
        }

        this.renderBody();
    }

    static get observedAttributes() {
        return ['src'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        // even though we only listen to src, be sure
        if (name === 'src') {
            this.src = newValue;
            this.load();
        }
    }
}

// Define the new element
customElements.define('query-table', DataTabler);
