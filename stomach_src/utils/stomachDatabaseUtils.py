from django.shortcuts import *
from stomach_src.models import *
import re


def getRecipeDetails(recipe_id, user_ID):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ing_Recipe.objects.all().filter(recipe_ID=recipe_id)
    tags = Tag_Recipe.objects.all().filter(recipe_ID=recipe_id)
    categories = Category_Recipe.objects.all().filter(recipe_ID=recipe_id)
    # check if user is the creator of the recipe in order to enable an edit function.
    try:
        Creator_Recipe.objects.get(recipe_ID=recipe_id, creator_ID=user_ID)
        isCreator = True
    except:
        isCreator = False

    try:
        isPublic = Creator_Recipe.objects.get(recipe_ID=recipe_id).public
    except:
        raise ValueError("recipe with id: " + recipe_id + " does not exist.")

    context = {'recipe': recipe, 'ingredients': ingredients, 'tags': tags, 'categories': categories,
               'userIsCreator': isCreator, 'isPublic': isPublic}
    return context

def createNewRecipe(request):
    creator_ID = request.user.id

    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())

    # post data
    name = dataDict["name"][0]
    description = dataDict["description"][0]
    cook_time = dataDict["cook_time"][0]
    person_amount = dataDict["person_amount"][0]
    ing_names = dataDict["form-0-name"]
    ing_unit_IDs = dataDict["form-0-unit"]
    ing_amounts = dataDict["form-0-amount"]
    category_IDs = dataDict["form-0-category"]

    # create new recipe
    newRecipe = Recipe.objects.create(name=name, description=description, cook_time=cook_time,
                                      person_amount=person_amount)
    newRecipe.publish()

    # create Creator_Recipe relation
    newCreatorRecipe = Creator_Recipe.objects.create(recipe_ID_id=newRecipe.id, creator_ID_id=creator_ID)
    if "public" in dataDict:
        public = dataDict["public"][0]
        if public == "on":
            newCreatorRecipe.public = True
    else:
        newCreatorRecipe.public = False
    newCreatorRecipe.save()

    # create new ingredients + ing_recipe relations
    # also add a tag for each ingredient's name.
    for i in range(0, len(ing_names)):
        # ingredient name + unit + amount
        # TODO: check for duplicates, should probably already happen on the frontend side.
        name = ing_names[i]
        unit = ing_unit_IDs[i]
        amount = ing_amounts[i]

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            newIngredient = Ingredient.objects.create(name=name)
        else:
            newIngredient = Ingredient.objects.all().get(name=name)

        # new ing_recipe relation
        Ing_Recipe.objects.create(unit=Unit.objects.get(id=unit), amount=amount, recipe_ID_id=newRecipe.id,
                                  ing_ID_id=newIngredient.id)

        # new tag where the name equals the name of the ingredient.
        newTag = Tag.objects.create(name=name)

        # new tag_recipe relation
        Tag_Recipe.objects.create(recipe_ID_id=newRecipe.id, tag_ID_id=newTag.id)

    # create category_Recipe relation
    for id in category_IDs:
        Category_Recipe.objects.create(recipe_ID_id=newRecipe.id, category_ID_id=id)

    return newRecipe.id

def create_new_storage(request):
    creator_ID = request.user.id

    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())

    # post data
    name = dataDict["name"][0]
    ing_names = dataDict["form-0-name"]
    ing_unit_IDs = dataDict["form-0-unit"]
    ing_amounts = dataDict["form-0-amount"]

    # create new storage
    newStorage = Storage.objects.create(name=name, user_ID_id=creator_ID)

    # create new ingredients and Storage_Ingredient relations
    for i in range(0, len(ing_names)):
        # ingredient name + unit + amount
        # TODO: check for duplicates, should probably already happen on the frontend side.
        name = ing_names[i]
        unit = ing_unit_IDs[i]
        amount = ing_amounts[i]

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            newIngredient = Ingredient.objects.create(name=name)
        else:
            newIngredient = Ingredient.objects.all().get(name=name)

        # new Storage_Ingredient relation
        Storage_Ingredient.objects.create(unit=Unit.objects.get(id=unit), amount=amount, ing_ID_id=newIngredient.id, storage_ID_id=newStorage.id)

    return newStorage.id