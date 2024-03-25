import asyncio

import aiopoke
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.biz_models import Pokemon

pokemon_router = APIRouter(tags=["pokemon"], prefix="/pokemon")


@pokemon_router.get("/{id}")
async def get_pokemon(id: int):
    async with (aiopoke.AiopokeClient() as client):
        try:
            res = await client.get_pokemon(id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"No pokemon with id '{id}'")
        else:
            if not res:
                raise HTTPException(status_code=404, detail="Failed to obtain Pokemon")
            return Pokemon(
                id=res.id,
                name=res.name,
                sprite=res.sprites.front_default.url,
                image=f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{id:03}.png"
            )


class PokemonListRequest(BaseModel):
    pokemon_ids: list[int]


@pokemon_router.post("")
async def get_many_pokemon(req: PokemonListRequest):
    tasks = []
    for pokemon_id in req.pokemon_ids:
        tasks.append(get_pokemon(pokemon_id))
    return await asyncio.gather(*tasks, return_exceptions=True)
