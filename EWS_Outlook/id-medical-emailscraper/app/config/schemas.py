from pydantic import BaseModel
from typing import List,Optional

class GHCSchema(BaseModel):
    UserName: Optional[str]
    Password: Optional[str]
    Host: Optional[str]
    ClientName: Optional[str]