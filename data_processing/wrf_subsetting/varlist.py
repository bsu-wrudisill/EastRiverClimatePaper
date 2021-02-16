## Comment OUT the variables you WANT to keep - all others will be excluded.  XTIME is neccessary for date transformations.

var_list = [
 'Times',   
 'XLAT',
 'XLONG',
 'LU_INDEX',
 'ZNU',
 'ZNW',
 'ZS',
 'DZS',
 'VAR_SSO',
 'U',
 'V',
 'W',
 'PH',
 'PHB',
 'T',
 'HFX_FORCE',
 'LH_FORCE',
 'TSK_FORCE',
 'HFX_FORCE_TEND',
 'LH_FORCE_TEND',
 'TSK_FORCE_TEND',
 'MU',
 'MUB',
 'NEST_POS',
 'P',
 'PB',
 'FNM',
 'FNP',
 'RDNW',
 'RDN',
 'DNW',
 'DN',
 'CFN',
 'CFN1',
 'THIS_IS_AN_IDEAL_RUN',
 'P_HYD',
 #'Q2',
 #'T2',
 'TH2',
 'PSFC',
 #'U10',
 #'V10',
 'RDX',
 'RDY',
 'RESM',
 'ZETATOP',
 'CF1',
 'CF2',
 'CF3',
 'ITIMESTEP',
 #'XTIME',
 'QVAPOR',
 'QCLOUD',
 'QRAIN',
 'QICE',
 'QSNOW',
 'QGRAUP',
 'QNICE',
 'QNRAIN',
 'SHDMAX',
 'SHDMIN',
 'SNOALB',
 'TSLB',
 'SMOIS',
 'SH2O',
 'SEAICE',
 'XICEM',
 'SFROFF',
 'UDROFF',
 'IVGTYP',
 'ISLTYP',
 'VEGFRA',
 'GRDFLX',
 'ACGRDFLX',
 'ACSNOM',
 'SNOW',
 'SNOWH',
 'CANWAT',
 'SSTSK',
 'COSZEN',
 'LAI',
 'VAR',
 'TKE_PBL',
 'EL_PBL',
 'MAPFAC_M',
 'MAPFAC_U',
 'MAPFAC_V',
 'MAPFAC_MX',
 'MAPFAC_MY',
 'MAPFAC_UX',
 'MAPFAC_UY',
 'MAPFAC_VX',
 'MF_VX_INV',
 'MAPFAC_VY',
 'F',
 'E',
 'SINALPHA',
 'COSALPHA',
 'HGT',
 'TSK',
 'P_TOP',
 'T00',
 'P00',
 'TLP',
 'TISO',
 'TLP_STRAT',
 'P_STRAT',
 'MAX_MSTFX',
 'MAX_MSTFY',
 'RAINC',
 'RAINSH',
 'RAINNC',
 'I_RAINC',
 'I_RAINNC',
 'SNOWNC',
 'GRAUPELNC',
 'HAILNC',
 'CLDFRA',
 #'SWDOWN',
 #'GLW',
 #'SWNORM',
 #'ACSWUPT',
 'ACSWUPTC',
 'ACSWDNT',
 'ACSWDNTC',
 'ACSWUPB',
 'ACSWUPBC',
 'ACSWDNB',
 'ACSWDNBC',
 'ACLWUPT',
 'ACLWUPTC',
 'ACLWDNT',
 'ACLWDNTC',
 'ACLWUPB',
 'ACLWUPBC',
 'ACLWDNB',
 'ACLWDNBC',
 'I_ACSWUPT',
 'I_ACSWUPTC',
 'I_ACSWDNT',
 'I_ACSWDNTC',
 'I_ACSWUPB',
 'I_ACSWUPBC',
 'I_ACSWDNB',
 'I_ACSWDNBC',
 'I_ACLWUPT',
 'I_ACLWUPTC',
 'I_ACLWDNT',
 'I_ACLWDNTC',
 'I_ACLWUPB',
 'I_ACLWUPBC',
 'I_ACLWDNB',
 'I_ACLWDNBC',
 #'SWUPB',
 'SWUPTC',
 'SWDNT',
 'SWDNTC',
 'SWUPB',
 'SWUPBC',
 'SWDNB',
 'SWDNBC',
 #'LWUPB',
 'LWUPTC',
 'LWDNT',
 'LWDNTC',
 'LWUPB',
 'LWUPBC',
 'LWDNB',
 'LWDNBC',
 #'OLR',
 'XLAT_U',
 'XLONG_U',
 'XLAT_V',
 'XLONG_V',
 #'ALBEDO',
 'CLAT',
 'ALBBCK',
 'EMISS',
 'NOAHRES',
 'ISNOW',
 'TV',
 'TG',
 'CANICE',
 'CANLIQ',
 'EAH',
 'TAH',
 'CM',
 'CH',
 #'FWET',
 'SNEQVO',
 'ALBOLD',
 'QSNOWXY',
 'WSLAKE',
 'ZWT',
 'WA',
 'WT',
 'TSNO',
 'ZSNSO',
 'SNICE',
 'SNLIQ',
 'LFMASS',
 'RTMASS',
 'STMASS',
 'WOOD',
 'GRAIN',
 'GDD',
 'STBLCP',
 'FASTCP',
 'XSAI',
 'TAUSS',
 'T2V',
 'T2B',
 'Q2V',
 'Q2B',
 'TRAD',
 'NEE',
 'GPP',
 'NPP',
 'FVEG',
 'QIN',
 'RUNSF',
 'RUNSB',
 'ECAN',
 'EDIR',
 'ETRAN',
 'FSA',
 'FIRA',
 'APAR',
 'PSN',
 'SAV',
 'SAG',
 'RSSUN',
 'RSSHA',
 'BGAP',
 'WGAP',
 'TGV',
 'TGB',
 'CHV',
 'CHB',
 'SHG',
 'SHC',
 'SHB',
 'EVG',
 'EVB',
 'GHV',
 'GHB',
 'IRG',
 'IRC',
 'IRB',
 'TR',
 'EVC',
 'CHLEAF',
 'CHUC',
 'CHV2',
 'CHB2',
 'CHSTAR',
 'SMCWTD',
 'RECH',
 'QRFS',
'QSPRINGS',
 'QSLAT',
 'TMN',
 'XLAND',
 'UST',
 'PBLH',
 #'HFX',
 'QFX',
 #'LH',
 'ACHFX',
 'ACLHF',
 'SNOWC',
 'SR',
 'SAVE_TOPO_FROM_REAL',
 'ISEEDARR_RAND_PERTURB',
 'ISEEDARR_SPPT',
 'ISEEDARR_SKEBS',
 'LANDMASK',
 'LAKEMASK',
 'SST',
 'SST_INPUT']
