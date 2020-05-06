import streamlit

CLUB = "&#9827;"
DIAMOND = "&#9826;"
HEART = "&#9825;"
SPADE = "&#9824;"

# Show individual hands in markdown format.
NORTH_MARKDOWN = "{} A9743\n{} K8763\n{} A6\n{}7".format(
        SPADE, HEART, DIAMOND, CLUB)
SOUTH_MARKDOWN = NORTH_MARKDOWN
WEST_MARKDOWN = NORTH_MARKDOWN
EAST_MARKDOWN = NORTH_MARKDOWN
for hand in [NORTH_MARKDOWN, SOUTH_MARKDOWN, WEST_MARKDOWN, EAST_MARKDOWN]:
    streamlit.markdown(hand)
