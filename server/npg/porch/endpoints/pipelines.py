# Copyright (C) 2021, 2022 Genome Research Ltd.
#
# Author: Kieron Taylor kt19@sanger.ac.uk
# Author: Marina Gourtovaia mg8@sanger.ac.uk
#
# This file is part of npg_porch
#
# npg_porch is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from starlette import status

from npg.porch.models.pipeline import Pipeline
from npg.porchdb.connection import get_DbAccessor

router = APIRouter(
    prefix="/pipelines",
    tags=["pipelines"]
)

@router.get(
    "/",
    response_model=List[Pipeline],
    summary="Get information about all pipelines.",
    description="Get all pipelines as a list. A uri filter can be used."
)
async def get_pipelines(db_accessor=Depends(get_DbAccessor)) -> List[Pipeline]:
    return await db_accessor.get_all_pipelines()

@router.get(
    "/{pipeline_name}",
    response_model=List[Pipeline],
    responses={404: {"description": "Not found"}},
    summary="Get information about versions of one pipeline.",
)
async def get_pipeline(pipeline_name: str,
                       pipeline_version: Optional[str]=None,
                       db_accessor=Depends(get_DbAccessor)
) -> List[Pipeline]:

    pipelines = await db_accessor.get_pipeline_by_name(name=pipeline_name, version=pipeline_version)
    if len(pipelines) == 0:
        raise HTTPException(status_code=404,
                            detail=f"Pipeline '{pipeline_name}' not found")
    return pipelines

@router.post(
    "/",
    response_model=Pipeline,
    summary="Create one pipeline record.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Pipeline was created"},
        409: {"description": "Pipeline already exists"}
    }
)
async def create_pipeline(pipeline: Pipeline, db_accessor=Depends(get_DbAccessor)) -> Pipeline:
    new_pipeline = None
    try:
        new_pipeline = await db_accessor.create_pipeline(pipeline)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail='Pipeline already exists')
    return new_pipeline
