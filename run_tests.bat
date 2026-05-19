@echo off
chcp 65001 >nul
echo ========================================
echo  接口自动化测试框架
echo ========================================
echo.

python -m pytest testcases/ -v

echo.
echo ========================================
echo  报告生成位置:
echo  - Allure报告: reports/allure-results
echo  - Excel报告: reports/test_report.xlsx
echo  - TXT报告: reports/test_summary.txt
echo  - 日志文件: logs/
echo ========================================
echo.

pause
