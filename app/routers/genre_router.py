from typing import List, Union

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, validator

####################
# Define Namespace #
####################
router = APIRouter(
    prefix="/genre",
    tags=["Music Genre"]
)


##################
# Req/Res Models #
##################
class MusicRecord(BaseModel):
    track_ID: Union[int, None]
    title: Union[str, None]
    tags: Union[str, None]
    loudness: Union[float, None]
    tempo: Union[float, None]
    time_signature: Union[int, None]
    key: Union[int, None]
    mode: Union[bool, None]
    duration: Union[float, None]
    vectors: List[Union[float, None]]

    # Check if the vectors list has 148 items (can be null)
    @validator("vectors")
    def check_vector_size(cls, v):
        assert len(v) == 148
        return v


class GenrePredictRequest(BaseModel):
    data: List[MusicRecord]


class GenrePredictResponse(BaseModel):
    title: str
    genre: str


#############
# Endpoints #
#############
@router.post("/predict",
             status_code=status.HTTP_200_OK,
             response_model=List[GenrePredictResponse],
             summary="Make prediction")
def predict(request_data: GenrePredictRequest):
    print(request_data)

    # TODO Make predictions
    # TODO Store predictions in DB
    # TODO Return predciton
    pass


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=List[str],
            summary="Retrieve the list of existing genre.")
def get_genre():
    # TODO Return unique list of the genre
    pass


@router.get("/{genre}/",
            status_code=status.HTTP_200_OK,
            response_model=List[str],
            summary="Get all music title from a specific genre")
def get_title(genre: str):
    # TODO return all music title with the genre
    return {genre: []}
