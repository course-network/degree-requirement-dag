
library(dplyr)
library(igraph)


reqs <- read.csv("./parse_course_requirements/edges.csv", header = F)
head(reqs)
names(reqs) <- c("course", "pre_rec")


req_net <- graph_from_data_frame(reqs, directed = T)
plot(req_net, directed = T)
tree_layout <- layout.reingold.tilford(req_net, root = "ST623", circular = FALSE, flip.y = FALSE)


# stat <- stat %>% select(ref, course, pre_rec, name)
# names(reqs) <- c("course", "ref", "pre_rec", "name")
# stat <- stat %>% select(ref, course, pre_rec, name)
# st_net <- graph_from_data_frame(stat, directed = T)
# plot(st_net)

st_net <- graph_from_data_frame(stat, directed = T)
plot(st_net)
plot(st_net, edge.color = stat$pre_rec, edge.curved = 0.3, edge.width = 2) # Thicker lines

# Calculate node degree
degree(st_net)
plot(st_net, vertex.color = degree(st_net))