"""Credit ledger — double-entry accounting for compute credits.

No blockchain. Credits are internal ledger entries.
Every transaction creates two entries: a debit and a credit.
This ensures the ledger always balances.

Design follows the Golem anti-pattern inversion:
- No wallet requirement
- No token
- No external blockchain dependency
- Just a Postgres table with ACID guarantees
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    """Types of credit transactions."""

    CONTRIBUTION = "contribution"    # Earned by providing compute
    CONSUMPTION = "consumption"      # Spent on using compute
    PURCHASE = "purchase"            # Bought with money (Stripe)
    BONUS = "bonus"                  # Sign-up bonus, referral, etc.
    ADJUSTMENT = "adjustment"        # Manual admin adjustment


class LedgerEntry(BaseModel):
    """A single ledger entry. Every transaction creates two entries (debit + credit)."""

    entry_id: str = Field(default_factory=lambda: str(uuid4()))
    transaction_id: str  # Groups debit + credit entries together
    account_id: str      # User or system account
    entry_type: str      # "debit" or "credit"
    amount: float        # Always positive; sign is determined by entry_type
    balance_after: float
    transaction_type: TransactionType
    description: str
    job_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Account(BaseModel):
    """A user's credit account."""

    account_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    balance: float = 0.0
    total_earned: float = 0.0     # Lifetime compute contributions
    total_spent: float = 0.0      # Lifetime compute consumption
    total_purchased: float = 0.0  # Lifetime credit purchases
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── SQL Schema (for Alembic migration) ──────────────────────

LEDGER_SCHEMA_SQL = """
-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    balance NUMERIC(18, 8) NOT NULL DEFAULT 0.0,
    total_earned NUMERIC(18, 8) NOT NULL DEFAULT 0.0,
    total_spent NUMERIC(18, 8) NOT NULL DEFAULT 0.0,
    total_purchased NUMERIC(18, 8) NOT NULL DEFAULT 0.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Double-entry ledger
CREATE TABLE IF NOT EXISTS ledger_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL,
    account_id UUID NOT NULL REFERENCES accounts(account_id),
    entry_type VARCHAR(6) NOT NULL CHECK (entry_type IN ('debit', 'credit')),
    amount NUMERIC(18, 8) NOT NULL CHECK (amount > 0),
    balance_after NUMERIC(18, 8) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    job_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_ledger_account ON ledger_entries(account_id);
CREATE INDEX IF NOT EXISTS idx_ledger_transaction ON ledger_entries(transaction_id);
CREATE INDEX IF NOT EXISTS idx_ledger_job ON ledger_entries(job_id) WHERE job_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_ledger_created ON ledger_entries(created_at);

-- Invariant: sum of all credits = sum of all debits (checked via trigger or app-level)
-- The system account absorbs the other side of contribution/purchase credits.
"""
