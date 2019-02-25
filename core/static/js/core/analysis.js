let appCalendarFrom = new Vue({
    el: '#calendarFrom',
    delimiters: ['[[', ']]'],
    data: {
        selectedDay: 1,
        selectedMonth: 1,
        selectedYear: 2020,
        onDateChange: undefined,
    },
    methods: {
        selectThisDay: function (e) {
            console.log("selectThisDay");
            let id = "day-" + e;
            $("#" + this.$el.id + " .one-day").removeClass("selected");
            $("#" + this.$el.id + " ." + id).addClass("selected");
            this.selectedDay = parseInt(e);
            $("#" + this.$el.id + " .all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        selectThisMonth: function (e) {
            console.log("selectThisMonth");
            let id = 'month-' + e;
            $("#" + this.$el.id + " .one-month").removeClass("selected");
            $("#" + this.$el.id + " ." + id).addClass("selected");
            this.selectedMonth = parseInt((id.replace('month-', '')));
            $("#" + this.$el.id + " .all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        selectThisYear: function (e) {
            console.log("selectThisYear");
            let id = 'year-' + e;
            $("#" + this.$el.id + " .one-year").removeClass("selected");
            $("#" + this.$el.id + " ." + id).addClass("selected");
            this.selectedYear = parseInt((id.replace('year-', '')));
            $("#" + this.$el.id + " .all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        openInputs(what) {
            $('.calendar .all').hide();
            $('#'+this.$el.id+' .all.'+what).fadeIn(300);
        }
    }
});

let appCalendarTo = new Vue({
    el: '#calendarTo',
    delimiters: ['[[', ']]'],
    data: {
        selectedDay: 1,
        selectedMonth: 1,
        selectedYear: 2020,
        onDateChange: undefined,
    },
    methods: {
        selectThisDay: function (e) {
            console.log("selectThisDay");
            let id = "day-" + e;
            $("#" + this.$el.id + " .one-day").removeClass("selected");
            $("#" + this.$el.id + " ." + id).addClass("selected");
            this.selectedDay = parseInt(e);
            $("#" + this.$el.id + " .all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        selectThisMonth: function (e) {
            console.log("selectThisMonth");
            let id = 'month-' + e;
            $("#" + this.$el.id + " .one-month").removeClass("selected");
            $("#" + this.$el.id + " ." + id).addClass("selected");
            this.selectedMonth = parseInt((id.replace('month-', '')));
            $("#" + this.$el.id + " .all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        selectThisYear: function (e) {
            console.log("selectThisYear");
            let id = 'year-' + e;
            $("#" + this.$el.id + " .one-year").removeClass("selected");
            $("#" + this.$el.id + " ." + id).addClass("selected");
            this.selectedYear = parseInt((id.replace('year-', '')));
            $("#" + this.$el.id + " .all").hide();

            if (this.onDateChange) {
                this.onDateChange();
            }
        },
        openInputs(what) {
            $('.calendar .all').hide();
            $('#'+this.$el.id+' .all.'+what).fadeIn(300);
        }
    }
});

let app = new Vue({
    el: '#display',
    delimiters: ['[[', ']]'],
    data: {
        targets: []
    },
    methods: {
        onDateChange: function () {
            $.ajax({
                url: '/laksa/get-analysis-data',
                data: {
                    "fromYear": appCalendarFrom.selectedYear,
                    "fromMonth": appCalendarFrom.selectedMonth,
                    "fromDay": appCalendarFrom.selectedDay,
                    "toYear": appCalendarTo.selectedYear,
                    "toMonth": appCalendarTo.selectedMonth,
                    "toDay": appCalendarTo.selectedDay,
                },
                success: function (data) {
                    let ldd = JSON.parse(data);
                    console.log(ldd)
                    app.targets = ldd;
                },
                error: function (data) {
                    alert("Ошибка при получении данных от сервера");
                    console.log(data.responseText);
                }
            })
        }
    },
    mounted: function() {
        appCalendarFrom.onDateChange = this.onDateChange;
        appCalendarTo.onDateChange = this.onDateChange;
    }
});