import pytest
import datetime
from sqlalchemy import select
from fastapi.exceptions import HTTPException

from npg.porchdb.models import Token, Pipeline
from npg.porchdb.auth import Validator
import npg.porch.models.permission
import npg.porch.models.pipeline

@pytest.mark.asyncio
async def test_token_string_is_valid(async_minimum):

    v = Validator(session = async_minimum)
    assert isinstance(v, (npg.porchdb.auth.Validator))
    # This token is an empty string.
    with pytest.raises(HTTPException):
        await v.token2permission("")
    # This token is too short.
    with pytest.raises(HTTPException):
        await v.token2permission('aaaa')
    # This token is too long.
    with pytest.raises(HTTPException):
        await v.token2permission('AAAAAAAAAAAAAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    # This token contains punctuation characters.
    with pytest.raises(HTTPException):
        await v.token2permission('7dc1457531e3495?9bd5:bcda579c1c6')
    # This token contains characters beyong F.
    with pytest.raises(HTTPException):
        await v.token2permission('7dc1457531e3495P9bd5Kbcda579c1c6')

@pytest.mark.asyncio
async def test_token_is_known_and_valid(async_minimum):

    v = Validator(session = async_minimum)

    # This token does not exist.
    with pytest.raises(HTTPException):
        await v.token2permission('doesnotexist11111111111111111111')

    # Mark one of the tokens as revoked.
    result = await async_minimum.execute(
        select(Token)
        .filter_by(description='OpenStack host, job finder')
    )
    token_row = result.scalar_one()
    token_string = token_row.token
    token_row.date_revoked = datetime.date(2022, 1, 1)
    async_minimum.add(token_row)
    await async_minimum.commit()

    with pytest.raises(HTTPException):
        await v.token2permission(token_string)

@pytest.mark.asyncio
async def test_permission_object_is_returned(async_minimum):

    # The fixtures have a token not associated with any pipeline.
    # To model data realistically, create a pipeline not associated
    # with any token.
    async_minimum.add(Pipeline(
        name='ptest ten',
        repository_uri='pipeline-testten.com',
        version='0.3.15'
    ))
    await async_minimum.commit()

    v = Validator(session = async_minimum)
    result = await async_minimum.execute(select(Token))
    token_rows = result.scalars().all()

    for t in token_rows:
        if t.description == 'Seqfarm host, job runner':
            p = await v.token2permission(t.token)
            assert isinstance(p, (npg.porch.models.permission.Permission))
            assert p.pipeline is not None
            assert isinstance(p.pipeline, (npg.porch.models.pipeline.Pipeline))
            assert p.pipeline.name == 'ptest one'
            assert p.requestor_id == t.token_id
            assert p.role == 'regular_user'
        elif t.description == 'Seqfarm host, admin':
            p = await v.token2permission(t.token)
            assert isinstance(p, (npg.porch.models.permission.Permission))
            assert p.pipeline is None
            assert p.requestor_id == t.token_id
            assert p.role == 'power_user'
