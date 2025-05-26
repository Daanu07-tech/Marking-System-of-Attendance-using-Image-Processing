@echo off

:: Delete contents of the dataset folder
if exist dataset\* (
    del /Q dataset\*
    echo Dataset folder contents deleted.
) else (
    echo Dataset folder is already empty or does not exist.
)

:: Delete contents of trainer.yml without deleting the file itself
if exist trainer\trainer.yml (
    echo. > trainer\trainer.yml
    echo Trainer.yml contents cleared.
) else (
    echo trainer.yml does not exist.
)

:: Delete face data files if they exist
if exist face_data.npy (
    del face_data.npy
    echo face_data.npy deleted.
) else (
    echo face_data.npy does not exist.
)

if exist face_data.csv (
    del face_data.csv
    echo face_data.csv deleted.
) else (
    echo face_data.csv does not exist.
)

:: Delete attendance files if they exist
if exist firebase\attendance_files\* (
    del /Q firebase\attendance_files\*
    echo Attendance files deleted.
) else (
    echo No attendance files to delete.
)

echo System reset completed.
pause
