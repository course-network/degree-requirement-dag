# cs_plot.R ------------------------------
#'
#'  Plot of CS data.
#'
# ....................................

<<<<<<< HEAD
library(dplyr)
library(igraph)

cs <- read.csv(file = "./course_data/csv/CS/CS_edge.csv", stringsAsFactors = F)
# Don't really need node info, just edges to create this plot
=======
>>>>>>> 40b4a8d9c75c87e69c56cdf3d15abf80ee595c81

# Create igraph object ------------------------------
cs_net <- graph_from_data_frame(cs, directed = T)

# Display CS ------------------------------

cs$or <- 1 + 1*(cs$course_dept == "OR")
cs$or_color <- c("grey", "steelblue")[cs$or]

V(cs_net)$label.cex = 0.65
E(cs_net)$arrow.size = 0.5
E(cs_net)$edge.color = cs$or_color
# V(cs_net)$vertex.size = 1
# plot.igraph(sub_net)

<<<<<<< HEAD
cs_layout <- layout_nicely(graph = cs_net)
=======
cs_layout <- layout_nicely(graph = sub_net)
>>>>>>> 40b4a8d9c75c87e69c56cdf3d15abf80ee595c81
plot(cs_net, directed = T,
     layout = cs_layout,
     edge.color = cs$or,
     vertex.size = 10,
     label.cex = 1,
     # vertex.size = sr_n$n * 1.5,
     vertex.shape = c("circle", "square")[grepl(x = names(V(cs_net)), pattern = "OR.+") + 1],
     vertex.color =  c("grey", "steelblue")[grepl(x = names(V(cs_net)), pattern = "OR.+") + 1])


# No scaling for size yet.
cs_n <- cs %>% group_by(pre_req) %>% summarise(n = n())
cs_n <- left_join(data.frame(names = names(V(cs_net))), cs_n, by = c("names" = "pre_req"))
head(cs_n)
cs_n$n[is.na(cs_n$n)] <- 0

plot(cs_net, directed = T,
     layout = cs_layout,
     edge.color = cs$or,
     vertex.size = 10,
     label.cex = 1,
     vertex.size = cs_n$n * 1.5,
     vertex.shape = c("circle", "square")[grepl(x = names(V(cs_net)), pattern = "OR.+") + 1],
     vertex.color =  c("grey", "steelblue")[grepl(x = names(V(cs_net)), pattern = "OR.+") + 1])

