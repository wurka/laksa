let app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        showNewTarget: false,
        authors: {
        },
        targets: {
        },
        showError: false,
        selectedDay: 1,
        selectedMonth: 1,
        selectedYear: 2019,
        selectedAuthor: undefined,
        selectedTarget: undefined,
        spendToday: [],
    },
    methods: {
        authorOnChange: function (e) {
            console.log("authorOnChange");
            console.log(e.target.value);
            this.selectedAuthor = e.target.value;
        },
        targetOnChange: function (e) {
            console.log("targetOnChange");
            console.log(e.target.value);
            this.selectedTarget = e.target.value;
        },
        selectThisDay: function (e) {
            console.log("selectThisDay");
            let id = "day-" + e;
            $(".one-day").removeClass("selected");
            $("#" + id).addClass("selected");
            this.selectedDay = parseInt(e);
            $(".all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        selectThisMonth: function (e) {
            console.log("selectThisMonth");
            let id = "month-"+e;
            $(".one-month").removeClass("selected");
            $("#" + id).addClass("selected");
            this.selectedMonth = parseInt(e);
            $(".all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        selectThisYear: function (e) {
            console.log("selectThisYear");
            let id = "year-"+e;
            $(".one-year").removeClass("selected");
            $("#" + id).addClass("selected");
            this.selectedYear = parseInt(e);
            $(".all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        onDateChange: function () {
            $.ajax({
                url: '/laksa/get-analysis-data',
                data: {
                    'fromYear': this.selectedYear,
                    'fromMonth': this.selectedMonth,
                    'fromDay': this.selectedDay,
                    'toYear': this.selectedYear,
                    'toMonth': this.selectedMonth,
                    'toDay': this.selectedDay,
                },
                success: function (data) {
                    app.spendToday = JSON.parse(data);
                },
                error: function (data) {
                    alert("Ошибка получения данных");
                    console.log(data.responseText);
                }
            });
        },
        submit: function () {
            if (
                (!this.selectedAuthor) ||
                (!this.selectedTarget) ||
                (!this.selectedYear) ||
                (!this.selectedMonth) ||
                (!this.selectedDay)) {
                return;
            }
            let year = this.selectedYear,
                month = this.selectedMonth,
                day = this.selectedDay,
                author = this.selectedAuthor,
                target = this.selectedTarget,
                howmuch = $('input[name=howmuch]').val();

            $.ajax({
                url: '/laksa/new-record',
                method: "POST",
                data: {
                    'year': year,
                    'month': month,
                    'day': day,
                    'author': author,
                    'target': target,
                    'howmuch': howmuch,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (data) {
                    console.log(data);
                    app.onDateChange();
                },
                error: function (data) {
                    alert("Ошибка добавления данных");
                    console.log(data.responseText);
                    app.onDateChange();
                }
            })


        }
    },
    mounted: function () {
        $(".new-target").show();
        let today = new Date(),
            year = today.getFullYear(),
            month = today.getMonth() + 1,
            day = today.getDate();

        this.selectThisYear(year);
        this.selectThisMonth(month);
        this.selectThisDay(day);

        $.ajax({
            url: '/laksa/get-authors',
            success: function (data) {
                app.authors = JSON.parse(data);
                $("select[name=who-select]").val(app.authors[0].id);
                app.selectedAuthor = app.authors[0].id;
                app.onDateChange();
            }
        });
        $.ajax({
            url: '/laksa/get-targets',
            success: function (data) {
                app.targets = JSON.parse(data);
                $("select[name=what-select]").val(app.targets[0].id);
                app.selectedTarget = app.targets[0].id;
                app.onDateChange();
            }
        });
    }
});