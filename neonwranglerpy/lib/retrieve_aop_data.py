"""Download AOP data around vst data for specified year, site."""
from neonwranglerpy.utilities.byTileAOP import by_tile_aop


def retrieve_aop_data(data, year=2019, dpID=['DP3.30006.001'], savepath=""):
    """Download AOP data around vst data for specified year, site.

    Parameters
    -----------
    data : pandas.DataFrame
        The vegetation structure dataframe having
        plotID, siteID, utmZone, easting, northing, year columns

    year : str
        Year for data to be downloaded

    dpID: list, str
        The NEON Data Product ID to be downloaded, in the form DPL.PRNUM.REV
        e.g. DP3.30006.001

    savepath : str
        The full path to the folder in which the files would be placed locally.
    """
    coords_for_tiles = data[[
        'plotID', 'siteID', 'utmZone', 'easting', 'northing', 'date'
    ]]
    # get tiles dimensions
    coords_for_tiles['easting'] = (coords_for_tiles[['easting']] / 1000) * 1000
    coords_for_tiles['northing'] = (coords_for_tiles[['northing']] / 1000) * 1000

    # drop duplicates values
    tiles = coords_for_tiles.drop_duplicates(
        subset=['siteID', 'utmZone', 'easting', 'northing', 'date']).reset_index(
            drop=True)
    tiles.dropna(axis=0, how='any', inplace=True)
    # convert CHEQ into STEI
    which_cheq = tiles['siteID'] == 'STEI'
    if which_cheq.any():
        which_easting = tiles['easting'] > 500000
        if which_easting.any:
            tiles.loc[which_cheq, "siteID"] = 'CHEQ'
            tiles.drop_duplicates(inplace=True)

    for i in range(tiles.shape[0]):
        for prd in dpID:
            try:
                tile = tiles.iloc[i, :]
                siteID, tile_year, tile_easting, tile_northing = tile['siteID'], tile[
                    'date'].split('-')[0], tile['easting'], tile['northing']
                by_tile_aop(prd,
                            siteID,
                            tile_year,
                            tile_easting,
                            tile_northing,
                            savepath=savepath)

            except Exception as e:
                print(f'site,{tile["siteID"]},could not be fully downloaded! Error in '
                      f'retrieving:{prd}, for year,{tile["year"]}, .error returned: {e}')
