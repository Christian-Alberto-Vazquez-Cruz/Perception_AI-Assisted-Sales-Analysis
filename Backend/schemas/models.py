from datetime import date
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator


class Sale(BaseModel):
    model_config = ConfigDict(extra='forbid')
    fecha: date
    categoria: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    unidades: Annotated[int, Field(strict=True, ge=0, le=1_000_000_000)]
    importe: Annotated[float, Field(ge=0, le=1_000_000_000_000, allow_inf_nan=False)]

    @field_validator('fecha', mode='before')
    @classmethod
    def iso_date(cls, value):
        if not isinstance(value, str) or len(value) != 10:
            raise ValueError('Usa fecha ISO YYYY-MM-DD')
        date.fromisoformat(value)
        return value

    @field_validator('importe', mode='before')
    @classmethod
    def numeric_amount(cls, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError('importe debe ser un número')
        return value


DatasetInput = Annotated[list[Sale], Field(min_length=1, max_length=100_000)]


class ChatInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    question: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]
    stream: bool = True
