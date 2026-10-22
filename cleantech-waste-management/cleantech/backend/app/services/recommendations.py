"""Editable disposal guidance, independent of the ML model. Keys are lowercase class names."""
DISCLAIMER = "Local municipal rules take precedence over this general guidance."
GUIDE = {
    "plastic": dict(disposal="Place clean plastics in the recycling bin if your local program accepts the resin type.",
        recycling="Check the resin code (1-7); rigid bottles and tubs are most widely accepted.",
        preparation="Empty, rinse, and remove caps if required locally.", warning="Food-soiled plastic and plastic film are often rejected."),
    "paper": dict(disposal="Recycle clean, dry paper.", recycling="Office paper, newspapers and magazines are widely accepted.",
        preparation="Keep dry; remove plastic wrapping.", warning="Greasy or wet paper (e.g. used napkins) contaminates recycling."),
    "cardboard": dict(disposal="Flatten and recycle dry cardboard.", recycling="Corrugated boxes are widely recycled.",
        preparation="Flatten boxes and remove tape and packing material.", warning="Pizza-box grease areas should be composted or binned."),
    "glass": dict(disposal="Recycle glass bottles and jars where accepted.", recycling="Glass is recyclable repeatedly.",
        preparation="Rinse and remove lids.", warning="Broken glass, mirrors and ceramics usually do not belong in glass recycling."),
    "metal": dict(disposal="Recycle clean metal cans and containers.", recycling="Aluminium and steel cans are highly recyclable.",
        preparation="Rinse; crush only if your program allows.", warning="Aerosols, batteries and paint cans need special handling."),
    "organic": dict(disposal="Compost food and garden waste where possible.", recycling="Home or municipal composting.",
        preparation="Separate from packaging.", warning="Avoid composting meat/dairy at home unless your system supports it."),
    "trash": dict(disposal="General waste: not identified as recyclable.", recycling="Probably not recyclable; consider reuse.",
        preparation="Bag securely.", warning="Hazardous items (batteries, electronics) need separate drop-off."),
}
GENERIC = dict(disposal="No specific guidance configured for this category.", recycling="Check local guidelines.",
               preparation="Keep items clean and dry.", warning="When unsure, ask your local waste authority.")

def get_recommendation(category: str) -> dict:
    return {**GUIDE.get(category.lower(), GENERIC), "disclaimer": DISCLAIMER}
