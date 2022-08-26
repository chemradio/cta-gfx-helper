let targetText = 'Украина еще в апреле была признана одной из самых заминированных стран мира. По оценке местной Государственной службы по чрезвычайным ситуациям (ГСЧС), минами и боеприпасами может быть загрязнена почти половина территории страны. Для полного разминирования земель, заминированных к середине августа, по прогнозу МВД Украины, может понадобиться от пяти до 10 лет. Наиболее заминированные области — Киевская и Черниговская; с начала апреля, после отступления российской армии, там обезвредили более 100 тысяч взрывоопасных предметов. По просьбе «Медузы» украинский фотограф Павел Дорогой съездил в Киевскую, Черниговскую и Сумскую области, где ведутся работы по разминированию, — и описал свои впечатления. А украинский журналист Василий Калына поговорил о разминировании Украины с саперами.';

const maxCharsPerLine = 20;
const minCharsPerLine = 20;

let procString = targetText;
let output = '';

while (true) {
    if (procString.length >= maxCharsPerLine) {
        let targetIndex = procString.slice(0,maxCharsPerLine).lastIndexOf(' ');

        let firstString = procString.slice(0,targetIndex);
        let secondString = procString.slice(targetIndex);

        while (true) {
            let lastWhite = firstString.lastIndexOf(' ');
            if ( (targetIndex - lastWhite) < 3) {}

        }

        // let splitStrings = [firstString, secondString];
        output += (firstString + '\n');
        procString = secondString;
    } else {
        output += procString;
        break
    }
}

console.log(output);
