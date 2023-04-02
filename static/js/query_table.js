import Fuse from './fuse.esm.js';

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
        min-width: 200px;
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
            width: 120px;
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
        this.keys = {
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
            universityDegree__universityDegreeUniversity: 'جامعة التخرج',
            universityDegree__universityDegreeCollege: 'كلية التخرج',
            universityDegree__universityDegreeSection: 'قسم التخرج',
            universityDegree__universityDegreeYear: 'سنة التخرج',
            universityDegree__universityDegreeAverage: 'معدل التخرج',
            specialization: 'التخصص',
            nominationDecision__nominationDecisionNumber: 'رقم قرار الترشيح',
            nominationDecision__nominationDecisionType: 'نوع قرار الترشيح',
            nominationDecision__nominationDecisionDate: 'تاريخ قرار الترشيح',
            certificateOfExcellence__certificateOfExcellenceYear:
                'سنة شهادة التفوق',
            certificateOfExcellence__certificateOfExcellenceDegree:
                'درجة شهادة التفوق',
            commencementAfterNominationDate: 'تاريخ المباشرة',
            residence: 'العنوان الحالي',
            mobile: 'رقم الهاتف المحمول',
            home: 'عنوان اﻹقامة',
            dispatch__dispatchDecisionNumber: 'رقم قرار الإيفاد',
            dispatch__freeze__freezeDecisionNumber: 'رقم قرار التجميد',
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

        const nav = document.createElement('div');
        nav.classList.add('px-3');
        const prevButton = document.createElement('button');
        prevButton.classList.add('btn', 'btn-outline-primary');
        prevButton.innerHTML = 'السابق';
        const nextButton = document.createElement('button');
        nextButton.classList.add('btn', 'btn-outline-primary', 'mx-2');
        nextButton.innerHTML = 'التالي';
        nav.append(prevButton, nextButton);

        div1.append(table);
        div1.classList.add('table-wrappe');

        shadow.append(div1, nav);

        // Attach the created elements to the shadow dom

        // https://www.freecodecamp.org/news/this-is-why-we-need-to-bind-event-handlers-in-class-components-in-react-f7ea1a6f93eb/
        this.sort = this.sort.bind(this);

        // this.nextPage = this.nextPage.bind(this);
        // this.previousPage = this.previousPage.bind(this);
        // this.search = this.search.bind(this);
        // this.changeSort = this.changeSort.bind(this);

        // nextButton.addEventListener('click', this.nextPage, false);
        // prevButton.addEventListener('click', this.previousPage, false);
    }

    load() {
        // error handling needs to be done :|
        
        this.data = [];
        let y = JSON.parse(this.src);
        y.forEach((o) => {
            let demon = {}
            
        });
        console.log(this.data);
        this.df = this.data;
        this.render();
    }

    render() {
        if (!this.cols) this.cols = Object.keys(this.data[0]);

        console.log(this.cols);

        this.renderHeader();
        // this.renderBody();
    }

    renderBody() {
        let result = '';
        let counter = 1;
        this.data.forEach((c) => {
            let r = `<tr>`;
            r += `<td>${counter}</td>`;
            counter++;
            this.cols.forEach((col) => {
                r += `<td>${c['fields'][col] ? c['fields'][col] : ''}</td>`;
            });
            r += '</tr>';
            result += r;
        });

        let tbody = this.shadowRoot.querySelector('tbody');
        tbody.innerHTML = result;
    }

    renderHeader() {
        let header = '<tr>';
        header += `<th scope='col' data-sort="id">#</th>`;
        this.cols.forEach((c) => {
            if (c !== 'id')
                header += `<th scope='col' data-sort="${c}">${this.keys[c]} </th>`;
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
                if (a['fields'][this.sortCol] < b['fields'][this.sortCol])
                    return this.sortAsc ? 1 : -1;
                if (a['fields'][this.sortCol] > b['fields'][this.sortCol])
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
