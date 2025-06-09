from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import uvicorn
from models import ExpenseCreate, ExpenseUpdate, ExpenseResponse, BalanceResponse, SettlementResponse, PersonResponse
from services import ExpenseService

app = FastAPI(
    title="Split App API",
    description="A FastAPI-based expense splitting backend system",
    version="1.0.0"
)

# Initialize the expense service
expense_service = ExpenseService()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Split App API is running",
        "version": "1.0.0",
        "endpoints": "/docs for API documentation"
    }

@app.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def add_expense(expense: ExpenseCreate):
    """Add a new expense"""
    try:
        new_expense = expense_service.add_expense(expense)
        # Convert datetime objects to ISO format strings
        expense_dict = new_expense.copy()
        expense_dict["created_at"] = new_expense["created_at"].isoformat()
        expense_dict["updated_at"] = new_expense["updated_at"].isoformat()
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Expense added successfully",
                "expense": expense_dict
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while adding expense: {str(e)}"
        )

@app.get("/expenses", response_model=List[Dict[str, Any]])
async def get_expenses():
    """Get all expenses"""
    try:
        expenses = expense_service.get_all_expenses()
        # Convert datetime objects to ISO format strings
        expenses_serializable = []
        for expense in expenses:
            expense_dict = expense.copy()
            expense_dict["created_at"] = expense["created_at"].isoformat()
            expense_dict["updated_at"] = expense["updated_at"].isoformat()
            expenses_serializable.append(expense_dict)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Retrieved {len(expenses)} expenses",
                "expenses": expenses_serializable
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving expenses: {str(e)}"
        )

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: int, expense_update: ExpenseUpdate):
    """Update an existing expense"""
    try:
        updated_expense = expense_service.update_expense(expense_id, expense_update)
        # Convert datetime objects to ISO format strings
        expense_dict = updated_expense.copy()
        expense_dict["created_at"] = updated_expense["created_at"].isoformat()
        expense_dict["updated_at"] = updated_expense["updated_at"].isoformat()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Expense updated successfully",
                "expense": expense_dict
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating expense: {str(e)}"
        )

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    """Delete an expense"""
    try:
        expense_service.delete_expense(expense_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Expense with ID {expense_id} deleted successfully"
            }
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting expense: {str(e)}"
        )

@app.get("/balances", response_model=List[BalanceResponse])
async def get_balances():
    """Get current balances for all people"""
    try:
        balances = expense_service.calculate_balances()
        # Convert Pydantic models to dictionaries
        balances_dict = [balance.dict() for balance in balances]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Balances calculated successfully",
                "balances": balances_dict
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while calculating balances: {str(e)}"
        )

@app.get("/settlements", response_model=List[SettlementResponse])
async def get_settlements():
    """Get simplified settlement summary with minimized transactions"""
    try:
        settlements = expense_service.calculate_settlements()
        # Convert Pydantic models to dictionaries
        settlements_dict = [settlement.dict() for settlement in settlements]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Settlements calculated successfully",
                "settlements": settlements_dict,
                "total_transactions": len(settlements)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while calculating settlements: {str(e)}"
        )

@app.get("/people", response_model=List[PersonResponse])
async def get_people():
    """Get all people who participated in expenses"""
    try:
        people = expense_service.get_all_people()
        # Convert Pydantic models to dictionaries
        people_dict = [person.dict() for person in people]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Retrieved {len(people)} people",
                "people": people_dict
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving people: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Split App API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
