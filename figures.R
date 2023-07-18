library(tidyverse)

#Aq. Sci.:For most journals the figures should be 39 mm, 84 mm, 129 mm, or 174 mm wide and not higher than 234 mm.
theme_pub <- theme_bw() + 
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(), 
        axis.text = element_text(colour = "black"), 
        strip.background = element_rect(fill = "white"))
theme_set(theme_pub)

images <- list.files("image_preproc", pattern=".png", full.names = TRUE, recursive = TRUE)

images_df <- tibble(paths = images) |> 
  separate(paths, into = c("dir", "set", "species", "image"), sep="/") |> 
  mutate(species = sub(" sp", "", species),
         source = ifelse(grepl("GBIF", image, fixed = TRUE), "GBIF", "Egne data"))

source_df <- images_df |> 
  group_by(species, source) |> 
  summarise(n = n()) |> 
  ungroup() |> 
  mutate(prop = n/sum(n),
         source = factor(source, levels=c("GBIF", "Egne data")),
         species = factor(species, levels=rev(sort(unique(images_df$species)))))

fig_data_dist <- source_df |> 
  ggplot(aes(factor(species), prop, fill=source)) +
  geom_col(position = position_stack())+
  scale_y_continuous(expand = expand_scale(c(0, 0.05)))+
  scale_fill_manual(values=c("purple", "orange"))+
  coord_flip()+
  ylab("Forekomst i datasæt (%)")+
  xlab("Taxa")+
  theme(legend.title = element_blank(), 
        legend.position = c(0.7, 0.3),
        axis.text.y = element_text(face = "italic"))

ggsave("figures/figure_3.png", fig_data_dist, height = 100, width = 129, units = "mm")
ggsave("figures/figure_3.pdf", fig_data_dist, height = 100, width = 129, units = "mm")
