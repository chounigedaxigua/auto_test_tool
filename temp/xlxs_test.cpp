#include <OpenXLSX.hpp>
#include <iostream>

void ReadWithOpenXLSX() {
    try {
        OpenXLSX::XLDocument doc;
        doc.open("example.xlsx");
        
        auto wks = doc.workbook().worksheet("Sheet1");
        
        // 读取单元格
        auto cell = wks.cell("A1");
        std::cout << "A1 value: " << cell.value().get<std::string>() << std::endl;
        
        // 或者使用行列号
        auto cell2 = wks.cell(1, 1); // 第1行第1列
        std::cout << "Cell(1,1): " << cell2.value().get<std::string>() << std::endl;
        
        doc.close();
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}