"""
Output Schema for PR Review Crew
Defines structured JSON format for code review results
"""

from pydantic import BaseModel, Field
from typing import List, Literal


class PRReviewOutput(BaseModel):
    """
    Structured output schema for Pull Request code review.
    Ensures consistent JSON format across all crew executions.
    """
    
    summary: str = Field(
        ...,
        description="Brief summary of total issues found (e.g., '5 issues found: 2 critical, 3 high priority')"
    )
    
    bugs: List[str] = Field(
        default_factory=list,
        description="List of critical bugs and security issues found"
    )
    
    optimizations: List[str] = Field(
        default_factory=list,
        description="List of performance optimization suggestions"
    )
    
    code_quality_issues: List[str] = Field(
        default_factory=list,
        description="List of code style and readability issues"
    )
    
    severity: Literal["critical", "high", "medium", "low"] = Field(
        ...,
        description="Overall severity level of issues found"
    )
    
    recommendation: Literal["Approve", "Approve with Changes", "Request Changes", "Reject"] = Field(
        ...,
        description="Final recommendation for the pull request"
    )
    
    critical_issues: List[str] = Field(
        default_factory=list,
        description="Issues that block PR merge"
    )
    
    high_priority: List[str] = Field(
        default_factory=list,
        description="Important issues strongly recommended to fix"
    )
    
    medium_priority: List[str] = Field(
        default_factory=list,
        description="Code quality improvements"
    )
    
    low_priority: List[str] = Field(
        default_factory=list,
        description="Nice-to-have enhancements"
    )
    
    files_reviewed: int = Field(
        default=0,
        description="Number of files reviewed in the PR"
    )
    
    lines_changed: int = Field(
        default=0,
        description="Total lines of code changed (additions + deletions)"
    )
    
    quality_score: int = Field(
        default=0,
        ge=0,
        le=10,
        description="Overall code quality score from 0-10"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "3 issues found: 1 critical, 2 high priority",
                "bugs": ["Possible null pointer in line 42 of helpers.js"],
                "optimizations": ["Use Promise.all for parallel requests in api.js"],
                "code_quality_issues": ["Inconsistent variable naming in utils.py"],
                "severity": "high",
                "recommendation": "Request Changes",
                "critical_issues": ["SQL injection vulnerability in database.py line 156"],
                "high_priority": ["Missing error handling in fetchData() function"],
                "medium_priority": ["Add docstrings to public methods"],
                "low_priority": ["Consider extracting magic numbers to constants"],
                "files_reviewed": 3,
                "lines_changed": 45,
                "quality_score": 6
            }
        }
