load_install <- function(.pkg){
    .has.pkg <- require(.pkg, character.only=T)
    if(!.has.pkg) {
        ## install once if needed
        install.packages(.pkg)
        .has.pkg <- require(.pkg, character.only=T)
        if(!.has.pkg) {
            stop(paste0('Please install package ', .pkg))
        }
    }
}
