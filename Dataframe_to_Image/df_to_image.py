import dataframe_image as dfi

def df_to_image(df, filename, rows = 5):
    """
    This function is used to create an image for any dataframe.
    """
    dfi.export(df.head(rows), f'static/{filename}.png')
