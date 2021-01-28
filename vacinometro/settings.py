BOT_NAME = "vacinometro"

SPIDER_MODULES = ["vacinometro.spiders"]
NEWSPIDER_MODULE = "vacinometro.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "vacinometro.pipelines.SyncVaccinesDataToGoogleSheetsPipeline": 500
}
