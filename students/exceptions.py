from fastapi import HTTPException, status

def student_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )