var app = new Vue({ 
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        showNewTarget: false,
        authors: {
            10: { name: "Саша"},
            20: { name: "Маша"},
            33: { name: "Саша и Маша"}
        },
        targets: {
            10: { title: "Проститутки" },
            12: { title: "Наркотики" },
            13: { title: "Оружие" },
            14: { title: "Проститутки" },
            15: { title: "Исподведь" }
        }
    },
    methods: {
        authorOnChange: function (e) {
            console.log("authorOnChange");
            console.log(e.target.value);
        },
        targetOnChange: function (e) {
            console.log("targetOnChange");
            console.log(e.target.value);
        }
    },
    mounted: function () {
        $(".new-target").show();
    }
});