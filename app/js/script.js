// Chest Pain Type Logic
const cpSelect = document.getElementById('cp-select');
const cpFields = ['ChestPainType_TA', 'ChestPainType_ATA', 'ChestPainType_NAP', 'ChestPainType_ASY'];

const cpMapping = {
    'TA': 'ChestPainType_TA',
    'ATA': 'ChestPainType_ATA',
    'NAP': 'ChestPainType_NAP',
    'ASY': 'ChestPainType_ASY'
};

cpSelect.addEventListener('change', function () {
    cpFields.forEach(field => document.getElementsByName(field)[0].value = '0');
    document.getElementsByName(cpMapping[cpSelect.value])[0].value = '1';
});
cpSelect.dispatchEvent(new Event('change'));


// Sex Logic
const sexSelect = document.getElementById('sex-select');
const sexMapping = {
    'M': 'Sex_M',
    'F': 'Sex_F'
};

sexSelect.addEventListener('change', function () {
    document.getElementsByName('Sex_M')[0].value = '0';
    document.getElementsByName('Sex_F')[0].value = '0';
    document.getElementsByName(sexMapping[sexSelect.value])[0].value = '1';
});
sexSelect.dispatchEvent(new Event('change'));


// Exercise Angina Logic
const exangSelect = document.getElementById('exang-select');
const exangMapping = {
    'Y': 'ExerciseAngina_Y',
    'N': 'ExerciseAngina_N'
};

exangSelect.addEventListener('change', function () {
    document.getElementsByName('ExerciseAngina_Y')[0].value = '0';
    document.getElementsByName('ExerciseAngina_N')[0].value = '0';
    document.getElementsByName(exangMapping[exangSelect.value])[0].value = '1';
});
exangSelect.dispatchEvent(new Event('change'));


// ST Slope Logic
const stSlopeSelect = document.getElementById('st-slope-select');
const stSlopeMapping = {
    'Up': 'ST_Slope_Up',
    'Flat': 'ST_Slope_Flat',
    'Down': 'ST_Slope_Down'
};

stSlopeSelect.addEventListener('change', function () {
    document.getElementsByName('ST_Slope_Up')[0].value = '0';
    document.getElementsByName('ST_Slope_Flat')[0].value = '0';
    document.getElementsByName('ST_Slope_Down')[0].value = '0';
    document.getElementsByName(stSlopeMapping[stSlopeSelect.value])[0].value = '1';
});
stSlopeSelect.dispatchEvent(new Event('change'));


// Resting ECG Logic
const restingECGSelect = document.getElementById('resting-ecg-select');
const restingECGMapping = {
    'Normal': 'RestingECG_Normal',
    'LVH': 'RestingECG_LVH',
    'ST': 'RestingECG_ST'
};

restingECGSelect.addEventListener('change', function () {
    document.getElementsByName('RestingECG_Normal')[0].value = '0';
    document.getElementsByName('RestingECG_LVH')[0].value = '0';
    document.getElementsByName('RestingECG_ST')[0].value = '0';
    document.getElementsByName(restingECGMapping[restingECGSelect.value])[0].value = '1';
});
restingECGSelect.dispatchEvent(new Event('change'));
