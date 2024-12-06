function createExcel(data, columns, fileName) {
    const ws = XLSX.utils.aoa_to_sheet([columns, ...data]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

    const wscols = [
        {wpx: 80},
        {wpx: 120},
        {wpx: 100},
        {wpx: 100},
        {wpx: 100}
    ];
    ws['!cols'] = wscols;

    XLSX.writeFile(wb, fileName);
}
function getDataFromInputs() {
    const data = [];
    const rows = document.querySelectorAll('table tbody tr');

    rows.forEach(row => {
        const rowData = [];

        const stt = row.querySelector('td:nth-child(1)').innerText;
        rowData.push(stt);

        const studentName = row.querySelector('td:nth-child(2)').innerText;
        rowData.push(studentName);

        const score15pInputs = row.querySelectorAll('[class^="EXAM_15P_"]');
        const score15pValues = Array.from(score15pInputs).map(input => input.value);
        const score15p = score15pValues.join(' ').trim() || null;
        rowData.push(score15p);

        const score45pInputs = row.querySelectorAll('[class^="EXAM_45P_"]');
        const score45pValues = Array.from(score45pInputs).map(input => input.value);
        const score45p = score45pValues.join(' ').trim() || null;
        rowData.push(score45p);

        const scoreThiInput = row.querySelector('.EXAM_final_1');
        const scoreThiValue = scoreThiInput.value.trim() || null;
        rowData.push(scoreThiValue);

        data.push(rowData);
    });

    return data;
}



document.getElementById('exportButton').addEventListener('click', function () {
    const data = getDataFromInputs();
    console.log(data);

    // Thay thế giá trị null bằng chuỗi rỗng
    const cleanedData = data.map(row => row.map(cell => cell === null ? 'None' : cell));

    const columns = ['STT', 'Tên Học Sinh', 'Điểm 15 phút', 'Điểm 45 phút', 'Điểm Thi'];
    createExcel(cleanedData, columns, 'student_scores.xlsx');
});