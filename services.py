from typing import List, Dict, Any
from datetime import datetime
from models import ExpenseCreate, ExpenseUpdate, BalanceResponse, SettlementResponse, PersonResponse

class ExpenseService:
    """Service class to handle expense operations and calculations"""
    
    def __init__(self):
        # In-memory storage
        self.expenses: List[Dict[str, Any]] = []
        self.next_id = 1
        
        # Pre-populate with test expenses as requested
        self._initialize_test_data()
    
    def _initialize_test_data(self):
        """Initialize with test expenses"""
        test_expenses = [
            {"amount": 600, "description": "Dinner", "paid_by": "Shantanu"},
            {"amount": 450, "description": "Groceries", "paid_by": "Sanket"},
            {"amount": 300, "description": "Petrol", "paid_by": "Om"},
            {"amount": 500, "description": "Movie Tickets", "paid_by": "Shantanu"},
            {"amount": 280, "description": "Pizza", "paid_by": "Sanket"}
        ]
        
        for expense_data in test_expenses:
            expense = ExpenseCreate(**expense_data)
            self.add_expense(expense)
    
    def add_expense(self, expense: ExpenseCreate) -> Dict[str, Any]:
        """Add a new expense"""
        now = datetime.now()
        new_expense = {
            "id": self.next_id,
            "amount": expense.amount,
            "description": expense.description,
            "paid_by": expense.paid_by,
            "created_at": now,
            "updated_at": now
        }
        
        self.expenses.append(new_expense)
        self.next_id += 1
        
        return new_expense
    
    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """Get all expenses"""
        return self.expenses.copy()
    
    def get_expense_by_id(self, expense_id: int) -> Dict[str, Any]:
        """Get expense by ID"""
        for expense in self.expenses:
            if expense["id"] == expense_id:
                return expense
        raise KeyError(f"Expense with ID {expense_id} not found")
    
    def update_expense(self, expense_id: int, expense_update: ExpenseUpdate) -> Dict[str, Any]:
        """Update an existing expense"""
        expense = self.get_expense_by_id(expense_id)
        
        # Update fields if provided
        if expense_update.amount is not None:
            expense["amount"] = expense_update.amount
        if expense_update.description is not None:
            expense["description"] = expense_update.description
        if expense_update.paid_by is not None:
            expense["paid_by"] = expense_update.paid_by
        
        expense["updated_at"] = datetime.now()
        
        return expense
    
    def delete_expense(self, expense_id: int) -> None:
        """Delete an expense"""
        expense = self.get_expense_by_id(expense_id)
        self.expenses.remove(expense)
    
    def get_all_people(self) -> List[PersonResponse]:
        """Get all people who participated in expenses"""
        people_data = {}
        
        for expense in self.expenses:
            person = expense["paid_by"]
            if person not in people_data:
                people_data[person] = {
                    "total_paid": 0,
                    "total_expenses": 0
                }
            
            people_data[person]["total_paid"] += expense["amount"]
            people_data[person]["total_expenses"] += 1
        
        # Calculate balances for each person
        balances = self._calculate_individual_balances()
        
        people = []
        for person, data in people_data.items():
            people.append(PersonResponse(
                name=person,
                total_paid=data["total_paid"],
                total_expenses=data["total_expenses"],
                balance=balances.get(person, 0)
            ))
        
        return sorted(people, key=lambda x: x.name)
    
    def _calculate_individual_balances(self) -> Dict[str, float]:
        """Calculate individual balances (internal method)"""
        if not self.expenses:
            return {}
        
        # Calculate total expenses and per-person share
        total_amount = sum(expense["amount"] for expense in self.expenses)
        unique_people = set(expense["paid_by"] for expense in self.expenses)
        num_people = len(unique_people)
        
        if num_people == 0:
            return {}
        
        per_person_share = total_amount / num_people
        
        # Calculate how much each person paid
        paid_by_person = {}
        for expense in self.expenses:
            person = expense["paid_by"]
            paid_by_person[person] = paid_by_person.get(person, 0) + expense["amount"]
        
        # Calculate balance for each person
        balances = {}
        for person in unique_people:
            amount_paid = paid_by_person.get(person, 0)
            balance = amount_paid - per_person_share
            balances[person] = round(balance, 2)
        
        return balances
    
    def calculate_balances(self) -> List[BalanceResponse]:
        """Calculate current balances for all people"""
        balances = self._calculate_individual_balances()
        
        balance_responses = []
        for person, balance in balances.items():
            if balance > 0.01:  # Gets money (others owe them)
                status = "gets"
            elif balance < -0.01:  # Owes money
                status = "owes"
            else:  # Even
                status = "even"
            
            balance_responses.append(BalanceResponse(
                person=person,
                balance=abs(balance),
                status=status
            ))
        
        return sorted(balance_responses, key=lambda x: x.person)
    
    def calculate_settlements(self) -> List[SettlementResponse]:
        """Calculate simplified settlements with minimized transactions"""
        balances = self._calculate_individual_balances()
        
        if not balances:
            return []
        
        # Separate people who owe money from those who should receive money
        debtors = []  # People who owe money (negative balance)
        creditors = []  # People who should receive money (positive balance)
        
        for person, balance in balances.items():
            if balance < -0.01:  # Owes money
                debtors.append({"person": person, "amount": abs(balance)})
            elif balance > 0.01:  # Gets money
                creditors.append({"person": person, "amount": balance})
        
        settlements = []
        
        # Sort by amount to optimize settlements
        debtors.sort(key=lambda x: x["amount"], reverse=True)
        creditors.sort(key=lambda x: x["amount"], reverse=True)
        
        # Calculate minimum transactions using greedy approach
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor = debtors[i]
            creditor = creditors[j]
            
            # Calculate settlement amount
            settlement_amount = min(debtor["amount"], creditor["amount"])
            
            if settlement_amount > 0.01:  # Only create settlement if amount is significant
                settlements.append(SettlementResponse(
                    from_person=debtor["person"],
                    to_person=creditor["person"],
                    amount=round(settlement_amount, 2)
                ))
                
                # Update remaining amounts
                debtor["amount"] -= settlement_amount
                creditor["amount"] -= settlement_amount
            
            # Move to next debtor/creditor if current one is settled
            if debtor["amount"] < 0.01:
                i += 1
            if creditor["amount"] < 0.01:
                j += 1
        
        return settlements
