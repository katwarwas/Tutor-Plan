from fastapi import HTTPException, status

def student_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

def teacher_authorized_exceptions():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nie masz uprawnień do usunięcia tego użytkownika"
    )