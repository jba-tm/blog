moment.locale('tk', {
    months : 'Ýanwar_Fewral_Mart_Aprel_Maý_Iýun_Iýul_Awgust_Sentýabr_Oktýabr_Noýabr_Dekabr'.split('_'),
    monthsShort : 'Ýan_Few_Mar_Apr_Maý_Iýn_Iýl_Awg_Sen_Okt_Noý_Dek'.split('_'),
    weekdays : 'Ýekşenbe_Duşenbe_Sişenbe_Çarşenbe_Penşenbe_Anna_Şenbe'.split('_'),
    weekdaysShort : 'Ýek_Duş_Siş_Çar_Pen_Anna_Şen'.split('_'),
    weekdaysMin : 'Ýe_Du_Si_Ça_Pe_An_Şe'.split('_'),
    longDateFormat : {
        LT : 'HH:mm',
        LTS : 'HH:mm:ss',
        L : 'DD.MM.YYYY',
        LL : 'D MMMM YYYY',
        LLL : 'D MMMM YYYY HH:mm',
        LLLL : 'dddd, D MMMM YYYY HH:mm'
    },
    calendar : {
        sameDay : '[şügün sagat] LT',
        nextDay : '[ertir sagat] LT',
        nextWeek : '[indiki hepde sagat] LT',
        lastDay : '[düýn sagat] LT',
        lastWeek : '[geçen hepde sagat] LT',
        sameElse : 'L'
    },
    relativeTime : {
        future : '%s soňra',
        past : '%s mundan ozal',
        s : 'birnäçe sekund',
        ss : '%d sekund',
        m : 'bir minut',
        mm : '%d minut',
        h : 'bir sagat',
        hh : '%d sagat',
        d : 'bir gün',
        dd : '%d gün',
        M : 'bir aý',
        MM : '%d aý',
        y : 'bir ýyl',
        yy : '%d ýyl'
    },
    ordinal: function (number, period) {
        switch (period) {
            case 'd':
            case 'D':
            case 'Do':
            case 'DD':
                return number;
            default:
                if (number === 0) {  // special case for zero
                    return number + '\'inji';
                }
                if (number === 6)
                var a = number % 10,
                    b = number % 100 - a,
                    c = number >= 100 ? 100 : null;
                return number + (suffixes$4[a] || suffixes$4[b] || suffixes$4[c]);
        }
    },
    week : {
        dow : 1, // Monday is the first day of the week.
        doy : 7  // The week that contains Jan 7th is the first week of the year.
    }
});