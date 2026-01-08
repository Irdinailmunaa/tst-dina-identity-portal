"""
Attendance Service Client - Ratu Integration
============================================

This module provides a client to interact with Ratu's Attendance Service API.
It handles JWT token generation and API communication for attendance operations.

Token Generation:
- Uses shared JWT_SECRET with Ratu
- Algorithm: HS256
- Expiry: 1 hour
- Claims: sub (user_id), iat, exp

Example Usage:
    client = AttendanceClient(
        base_url="https://ratu.theokaitou.my.id",
        jwt_secret="RatuDinaTST2026_",
        jwt_alg="HS256"
    )
    
    # Get attendance for event
    attendance = await client.get_attendance("E001")
    
    # Create check-in
    checkin = await client.create_checkin("E001", "T001", "user1")
"""

import os
import jwt
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException


class AttendanceClient:
    """Client for Ratu Attendance Service API"""
    
    def __init__(
        self,
        base_url: str,
        jwt_secret: str,
        jwt_alg: str = "HS256",
        timeout: float = 20.0
    ):
        """
        Initialize AttendanceClient
        
        Args:
            base_url: Base URL of Ratu attendance service
            jwt_secret: JWT secret key (shared with Ratu)
            jwt_alg: JWT algorithm (default: HS256)
            timeout: HTTP request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.jwt_secret = jwt_secret
        self.jwt_alg = jwt_alg
        self.timeout = timeout
    
    def _generate_token(self, user_id: str) -> str:
        """
        Generate JWT token for Ratu API authentication
        
        Args:
            user_id: User ID to embed in token
            
        Returns:
            JWT token string
        """
        now = datetime.utcnow()
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(hours=1)
        }
        token = jwt.encode(
            payload,
            self.jwt_secret,
            algorithm=self.jwt_alg
        )
        return token
    
    async def get_attendance(
        self,
        event_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get attendance summary for an event from Ratu
        
        Args:
            event_id: Event ID to get attendance for
            user_id: User ID requesting the data (for token generation)
            
        Returns:
            Attendance data from Ratu
            
        Raises:
            HTTPException: If request fails or event not found
            
        Example Response:
            {
                "event_id": "E001",
                "event_name": "Tech Conference 2026",
                "total_registered": 150,
                "total_checked_in": 87,
                "checkin_percentage": 58,
                "checkins": [...]
            }
        """
        token = self._generate_token(user_id)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/api/attendance/{event_id}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 401:
                    raise HTTPException(
                        status_code=401,
                        detail="Authentication failed - token invalid or expired"
                    )
                elif response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Event '{event_id}' not found"
                    )
                elif response.status_code >= 500:
                    raise HTTPException(
                        status_code=502,
                        detail="Attendance service temporarily unavailable"
                    )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Attendance service request timeout"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to reach attendance service: {str(e)}"
            )
    
    async def create_checkin(
        self,
        event_id: str,
        ticket_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Create a new check-in record in Ratu
        
        Args:
            event_id: Event ID for the check-in
            ticket_id: Ticket ID being checked in
            user_id: User ID requesting the check-in
            
        Returns:
            Check-in confirmation from Ratu
            
        Raises:
            HTTPException: If check-in fails
            
        Example Response:
            {
                "checkin_id": "C002",
                "event_id": "E001",
                "ticket_id": "T001",
                "user_id": "user1",
                "checkin_time": "2026-01-08T10:35:00Z",
                "status": "success"
            }
        """
        token = self._generate_token(user_id)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "event_id": event_id,
            "ticket_id": ticket_id
        }
        
        url = f"{self.base_url}/api/checkins"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=headers, json=body)
                
                if response.status_code == 401:
                    raise HTTPException(
                        status_code=401,
                        detail="Authentication failed - token invalid or expired"
                    )
                elif response.status_code == 400:
                    data = response.json()
                    raise HTTPException(
                        status_code=400,
                        detail=data.get("detail", "Invalid check-in request")
                    )
                elif response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail="Event or ticket not found"
                    )
                elif response.status_code >= 500:
                    raise HTTPException(
                        status_code=502,
                        detail="Attendance service temporarily unavailable"
                    )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Attendance service request timeout"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to reach attendance service: {str(e)}"
            )
    
    async def get_user_checkins(
        self,
        user_id: str,
        event_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all check-ins for a user (optionally filtered by event)
        
        Args:
            user_id: User ID to get check-ins for
            event_id: Optional event ID to filter check-ins
            
        Returns:
            User's check-in records
            
        Raises:
            HTTPException: If request fails
            
        Example Response:
            {
                "user_id": "user1",
                "checkins": [
                    {
                        "checkin_id": "C001",
                        "event_id": "E001",
                        "event_name": "Tech Conference 2026",
                        "ticket_id": "T001",
                        "checkin_time": "2026-01-08T10:30:00Z"
                    },
                    ...
                ]
            }
        """
        token = self._generate_token(user_id)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/api/checkins"
        params = {}
        if event_id:
            params["event_id"] = event_id
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, params=params)
                
                if response.status_code == 401:
                    raise HTTPException(
                        status_code=401,
                        detail="Authentication failed - token invalid or expired"
                    )
                elif response.status_code >= 500:
                    raise HTTPException(
                        status_code=502,
                        detail="Attendance service temporarily unavailable"
                    )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Attendance service request timeout"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to reach attendance service: {str(e)}"
            )
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check if Ratu attendance service is healthy
        
        Returns:
            Health status from Ratu
            
        Raises:
            HTTPException: If service is unavailable
        """
        url = f"{self.base_url}/health"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
                
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Attendance service unhealthy: {str(e)}"
            )


def create_attendance_client() -> AttendanceClient:
    """
    Factory function to create AttendanceClient with environment variables
    
    Returns:
        Configured AttendanceClient instance
        
    Raises:
        RuntimeError: If required environment variables are missing
    """
    base_url = os.getenv("ATTENDANCE_BASE_URL")
    jwt_secret = os.getenv("JWT_SECRET")
    jwt_alg = os.getenv("JWT_ALG", "HS256")
    
    if not base_url:
        raise RuntimeError("ATTENDANCE_BASE_URL environment variable not set")
    if not jwt_secret:
        raise RuntimeError("JWT_SECRET environment variable not set")
    
    return AttendanceClient(
        base_url=base_url,
        jwt_secret=jwt_secret,
        jwt_alg=jwt_alg
    )
